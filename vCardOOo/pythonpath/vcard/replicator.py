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

from .unotool import getDateTime

from .database import DataBase
from .dataparser import DataParser
from .addressbook import AddressBook

from .configuration import g_sync
from .configuration import g_filter

from .logger import logMessage
from .logger import getMessage
g_message = 'replicator'

from threading import Thread
from threading import Event
from threading import Condition
import traceback


class Replicator(unohelper.Base):
    def __init__(self, ctx, database, users):
        self._ctx = ctx
        self._database = database
        self._users = users
        self._started = Event()
        self._paused = Event()
        self._disposed = Event()
        self._count = 0
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

    def _replicate(self):
        print("replicator.run()1")
        try:
            print("replicator.run()1 begin ****************************************")
            while not self._disposed.is_set():
                print("replicator.run()2 wait to start ****************************************")
                self._started.wait()
                if not self._disposed.is_set():
                    print("replicator.run()3 synchronize started ****************************************")
                    self._count = 0
                    dltd, mdfd = self._synchronize()
                    self._database.dispose()
                    print("replicator.run()4 synchronize ended query=%s deleted=%s modified=%s *******************************************" % (dltd + mdfd, dltd, mdfd))
                    if self._started.is_set():
                        print("replicator.run()5 start waitting *******************************************")
                        self._paused.clear()
                        self._paused.wait(g_sync)
                        print("replicator.run()5 end waitting *******************************************")
            print("replicator.run()6 canceled *******************************************")
        except Exception as e:
            msg = "Replicator run(): Error: %s" % traceback.print_exc()
            print(msg)

    def _synchronize(self):
        dltd = mdfd = 0
        for user in self._users.values():
            if self._canceled():
                break
            if user.isOffLine():
                msg = getMessage(self._ctx, g_message, 101)
                logMessage(self._ctx, INFO, msg, 'Replicator', '_synchronize()')
            elif not self._canceled():
                dltd, mdfd = self._syncUser(user, dltd, mdfd)
        return dltd, mdfd

    def _syncUser(self, user, dltd, mdfd):
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
            if not self._canceled():
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
        self._database.Connection.commit()
        self._database.setLoggingChanges(True)
        self._database.saveChanges()
        self._database.Connection.setAutoCommit(True)


    def _syncData(self):
        result = KeyMap()
        timestamp = getDateTime(False)

        self._database.setLoggingChanges(False)
        self._database.saveChanges()
        self._database.Connection.setAutoCommit(False)

        for user in self.Users.values():
            if not self._canceled():
                msg = getMessage(self._ctx, g_message, 111, user.Account)
                logMessage(self._ctx, INFO, msg, 'Replicator', '_synchronize()')
                result.setValue(user.Account, self._syncUser1(user, timestamp))
                msg = getMessage(self._ctx, g_message, 112, user.Account)
                logMessage(self._ctx, INFO, msg, 'Replicator', '_synchronize()')
        if not self._canceled():
            self._database.executeBatchCall()
            self._database.Connection.commit()
            for account in result.getKeys():
                user = self.Users[account]
                user.MetaData += result.getValue(account)
                print("Replicator._syncData(): %s" % (user.MetaData, ))
                self._syncConnection(user, timestamp)
        self._database.executeBatchCall()

        self._database.Connection.commit()
        self._database.setLoggingChanges(True)
        self._database.saveChanges()
        self._database.Connection.setAutoCommit(True)

    def _syncUser1(self, user, timestamp):
        result = KeyMap()
        try:
            if self._canceled():
                return result
            result += self._syncPeople(user, timestamp)
            if self._canceled():
                return result
            result += self._syncGroup(user, timestamp)
        except Exception as e:
            msg = getMessage(self._ctx, g_message, 121, (e, traceback.print_exc()))
            logMessage(self._ctx, SEVERE, msg, 'Replicator', '_synchronize()')
        return result

    def _syncPeople(self, user, timestamp):
        token = None
        method = {'Name': 'People',
                  'PrimaryKey': 'Resource',
                  'ResourceFilter': (),
                  'Deleted': (('metadata','deleted'), True),
                  'Filter': (('metadata', 'primary'), True),
                  'Skip': ('Type', 'metadata')}
        pages = update = delete = 0
        parameter = self.Provider.getRequestParameter(method['Name'], user)
        parser = DataParser(self._database, self.Provider, method['Name'])
        map = self._database.getFieldsMap(method['Name'], False)
        enumerator = user.Request.getEnumeration(parameter, parser)
        while not self._canceled() and enumerator.hasMoreElements():
            response = enumerator.nextElement()
            if response.IsPresent:
                pages += 1
                u, d, t = self._syncResponse(method, user, map, response.Value, timestamp)
                update += u
                delete += d
                token = t
        format = (pages, update, delete)
        msg = getMessage(self._ctx, g_message, 131, format)
        logMessage(self._ctx, INFO, msg, 'Replicator', '_syncPeople()')
        self._count += update + delete
        print("replicator._syncPeople() 1 %s" % method['PrimaryKey'])
        return token

    def _syncGroup(self, user, timestamp):
        token = None
        method = {'Name': 'Group',
                  'PrimaryKey': 'Resource',
                  'ResourceFilter': (('groupType', ), g_filter),
                  'Deleted': (('metadata','deleted'), True)}
        pages = update = delete = 0
        parameter = self.Provider.getRequestParameter(method['Name'], user)
        parser = DataParser(self._database, self.Provider, method['Name'])
        map = self._database.getFieldsMap(method['Name'], False)
        enumerator = user.Request.getEnumeration(parameter, parser)
        while not self._canceled() and enumerator.hasMoreElements():
            response = enumerator.nextElement()
            if response.IsPresent:
                pages += 1
                u, d, t = self._syncResponse(method, user, map, response.Value, timestamp)
                update += u
                delete += d
                token = t
        format = (pages, update, delete)
        msg = getMessage(self._ctx, g_message, 141, format)
        logMessage(self._ctx, INFO, msg, 'Replicator', '_syncGroup()')
        self._count += update + delete
        return token

    def _syncConnection(self, user, timestamp):
        token = None
        pages = update = delete = 0
        groups = self._database.getUpdatedGroups(user, 'contactGroups/')
        if groups.Count > 0:
            for group in groups:
                name = group.getValue('Name')
                group = group.getValue('Group')
                self._database.createGroupView(user, name, group)
            print("replicator._syncConnection(): %s" % ','.join(groups.getKeys()))
            method = {'Name': 'Connection',
                      'PrimaryKey': 'Group',
                      'ResourceFilter': ()}
            parameter = self.Provider.getRequestParameter(method['Name'], groups)
            parser = DataParser(self._database, self.Provider, method['Name'])
            map = self._database.getFieldsMap(method['Name'], False)
            request = user.Request.getRequest(parameter, parser)
            response = request.execute()
            if response.IsPresent:
                pages += 1
                u, d, token = self._syncResponse(method, user, map, response.Value, timestamp)
                update += u
        else:
            print("replicator._syncConnection(): nothing to sync")
        format = (pages, len(groups), update)
        msg = getMessage(self._ctx, g_message, 151, format)
        logMessage(self._ctx, INFO, msg, 'Replicator', '_syncConnection()')
        self._count += update
        return token

    def _syncResponse(self, method, user, map, data, timestamp):
        update = delete = 0
        token = None
        for key in data.getKeys():
            field = map.getValue(key).getValue('Type')
            if field == 'Field':
                token = self._database.updateSyncToken(user, key, data, timestamp)
            elif field != 'Header':
                u, d = self._mergeResponse(method, user, map, key, data.getValue(key), timestamp, field)
                update += u
                delete += d
        return update, delete, token

    def _mergeResponse(self, method, user, map, key, data, timestamp, field):
        update = delete = 0
        if field == 'Sequence':
            f = map.getValue(key).getValue('Table')
            for d in data:
                u , d, = self._mergeResponse(method, user, map, key, d, timestamp, f)
                update += u
                delete += d
        elif data.hasValue(method['PrimaryKey']):
            if self._filterResponse(data, *method['ResourceFilter']):
                resource = data.getValue(method['PrimaryKey'])
                update, delete = self._getMerge(method, resource, user, map, data, timestamp)
        return update, delete

    def _filterResponse(self, data, filters=(), value=None, index=0):
        if index < len(filters):
            filter = filters[index]
            if data.hasValue(filter):
                return self._filterResponse(data.getValue(filter), filters, value, index + 1)
            return False
        return data if value is None else data == value

    def _getMerge(self, method, resource, user, map, data, timestamp):
        name = method['Name']
        if name == 'People':
            update, delete = self._mergePeople(method, resource, user, map, data, timestamp)
        elif name == 'Group':
            update, delete = self._mergeGroup(method, resource, user, map, data, timestamp)
        elif name == 'Connection':
            update, delete = self._mergeConnection(method, resource, user, map, data, timestamp)
        return update, delete

    def _mergePeople(self, method, resource, user, map, data, timestamp):
        update = delete = 0
        deleted = self._filterResponse(data, *method['Deleted'])
        update, delete = self._database.mergePeople(user, resource, timestamp, deleted)
        for key in data.getKeys():
            if key == method['PrimaryKey']:
                continue
            f = map.getValue(key).getValue('Type')
            update += self._mergePeopleData(method, map, resource, key, data.getValue(key), timestamp, f)
        return update, delete

    def _mergeGroup(self, method, resource, user, map, data, timestamp):
        update = delete = 0
        name = data.getDefaultValue('Name', '')
        deleted = self._filterResponse(data, *method['Deleted'])
        update, delete = self._database.mergeGroup(user, resource, name, timestamp, deleted)
        return update, delete

    def _mergeConnection(self, method, resource, user, map, data, timestamp):
        update = self._database.mergeConnection(user, resource, timestamp)
        return update, 0

    def _mergePeopleData(self, method, map, resource, key, data, timestamp, field):
        update = 0
        if field == 'Sequence':
            f = map.getValue(key).getValue('Table')
            for d in data:
                update += self._mergePeopleData(method, map, resource, key, d, timestamp, f)
        elif field == 'Tables':
            if self._filterResponse(data, *method['Filter']):
                default = self._default.get(key, None)
                typename = data.getDefaultValue('Type', default)
                for label in data.getKeys():
                    if label in method['Skip']:
                        continue
                    value = data.getValue(label)
                    update += self._database.mergePeopleData(key, resource, typename, label, value, timestamp)
        return update
