#!
# -*- coding: utf_8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020 https://prrvchr.github.io                                     ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

import uno
import unohelper

from com.sun.star.util import XCancellable
from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from .unolib import KeyMap

from .unotool import executeDispatch
from .unotool import getConfiguration
from .unotool import getDateTime
from .unotool import getNamedValueSet

from .database import DataBase
from .dataparser import DataParser
from .addressbook import AddressBook

from .configuration import g_identifier
from .configuration import g_filter

from .logger import Pool
from .logger import logMessage
from .logger import getMessage
g_message = 'Replicator'

from threading import Thread
from threading import Event
from threading import Condition
import traceback


class Replicator(unohelper.Base):
    def __init__(self, ctx, database, users):
        self._ctx = ctx
        self._cardsync = '%s.CardSync' % g_identifier
        self._database = database
        self._users = users
        self._started = Event()
        self._paused = Event()
        self._disposed = Event()
        self._thread = Thread(target=self._replicate)
        self._thread.start()

    # XRestReplicator
    def dispose(self):
        print("replicator.dispose() 1")
        self._disposed.set()
        self._started.set()
        self._paused.set()
        self._thread.join()
        print("replicator.dispose() 2")

    def stop(self):
        print("replicator.stop() 1")
        self._started.clear()
        self._paused.set()
        print("replicator.stop() 2")

    def start(self):
        self._started.set()
        self._paused.set()

    def _canceled(self):
        return False

    def _canceled1(self):
        return self._disposed.is_set() or not self._started.is_set()

    def _getReplicateTimeout(self):
        configuration = getConfiguration(self._ctx, g_identifier, False)
        timeout = configuration.getByName('ReplicateTimeout')
        return timeout

    def _replicate(self):
        print("replicator.run()1")
        try:
            print("replicator.run()1 begin ****************************************")
            logger = Pool(self._ctx).getLogger('Replicator')
            while not self._disposed.is_set():
                print("replicator.run()2 wait to start ****************************************")
                self._started.wait()
                if not self._disposed.is_set():
                    print("replicator.run()3 synchronize started ****************************************")
                    dltd, mdfd = self._synchronize(logger)
                    total = dltd + mdfd
                    if total > 0:
                        url = 'vnd.sun.star.job:service=%s' % self._cardsync 
                        arguments = getNamedValueSet({'Connection': self._database.Connection})
                        executeDispatch(self._ctx, url, arguments)
                    self._database.dispose()
                    format = total, mdfd, dltd
                    logger.logResource(INFO, 101, format, 'Replicator', '_replicate()')
                    print("replicator.run()4 synchronize ended query=%s deleted=%s modified=%s *******************************************" % (dltd + mdfd, dltd, mdfd))
                    if self._started.is_set():
                        print("replicator.run()5 start waitting *******************************************")
                        self._paused.clear()
                        timeout = self._getReplicateTimeout()
                        self._paused.wait(timeout)
                        print("replicator.run()5 end waitting *******************************************")
            print("replicator.run()6 canceled *******************************************")
        except Exception as e:
            msg = "Replicator run(): Error: %s" % traceback.print_exc()
            print(msg)

    def _synchronize(self, logger):
        dltd = mdfd = 0
        for user in self._users.values():
            if self._canceled():
                break
            if user.isOffLine():
                logger.logResource(INFO, 111, None, 'Replicator', '_synchronize()')
            elif not self._canceled():
                logger.logResource(INFO, 112, user.Name, 'Replicator', '_synchronize()')
                dltd, mdfd = self._syncUser(logger, user, dltd, mdfd)
                logger.logResource(INFO, 113, user.Name, 'Replicator', '_synchronize()')
        return dltd, mdfd

    def _syncUser(self, logger, user, dltd, mdfd):
        for aid in user.getAddressbooks():
            if self._canceled():
                break
            addressbook = AddressBook(self._ctx, self._database, user, aid)
            print("Replicator._syncUser() %s" % (addressbook.New, ))
            if addressbook.New:
                cards = addressbook.getAddressbookCards()
                mdfd += self._mergeCard(addressbook, cards)
                if not self._canceled():
                    self._database.updateAddressbookToken(addressbook.Id, addressbook.AdrSync)
            elif not self._canceled():
                dltd, mdfd = self._pullModifiedCard(addressbook, dltd, mdfd)
        return dltd, mdfd

    def _mergeCard(self, addressbook, cards):
        mdfd = 0
        self._setBatchModeOn()
        for card in cards:
            if self._canceled():
                break
            print("Replicator._mergeCard() %s" % (card, ))
            mdfd += self._database.mergeCard(addressbook.Id, *card)
        if not self._canceled():
            self._database.executeBatchCall()
            self._database.Connection.commit()
        self._setBatchModeOff()
        return mdfd

    def _pullModifiedCard(self, addressbook, dltd, mdfd):
        if addressbook.AdrSync is not None:
            dltd, mdfd = self._pullModifiedCardByToken(addressbook, dltd, mdfd)
        elif addressbook.Tag is not None:
            dltd, mdfd = self._pullModifiedCardByTag(addressbook, dltd, mdfd)
        else:
            print("Replicator._pullModifiedCard() Error %s" % (addressbook.Name, ))
        return dltd, mdfd

    def _pullModifiedCardByToken(self, addressbook, dltd, mdfd):
        print("Replicator._pullModifiedCardByToken() %s" % (addressbook.Name, ))
        token, modified, deleted = addressbook.getModifiedCardByToken()
        if addressbook.AdrSync != token:
            if deleted:
                dltd += self._database.deleteCard(addressbook.Id, deleted)
            if modified:
                cards = addressbook.getModifiedCard(modified)
                mdfd += self._mergeCard(addressbook, cards)
            self._database.updateAddressbookToken(addressbook.Id, token)
        return dltd, mdfd

    def _pullModifiedCardByTag(self, addressbook, dltd, mdfd):
        print("Replicator._pullModifiedCardByTag() %s" % (addressbook.Name, ))
        return dltd, mdfd

    def _setBatchModeOn(self):
        self._database.setLoggingChanges(False)
        self._database.saveChanges()
        self._database.Connection.setAutoCommit(False)

    def _setBatchModeOff(self):
        self._database.setLoggingChanges(True)
        self._database.saveChanges()
        self._database.Connection.setAutoCommit(True)
