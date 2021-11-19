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

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from com.sun.star.sdb.CommandType import QUERY

from com.sun.star.sdbc import XRestDataSource

from .configuration import g_identifier
from .configuration import g_group
from .configuration import g_compact

from .database import DataBase
#from .provider import Provider

from .user import User
from .user import getUserId

from .addressbook import AddressBook
from .addressbook import getAddressbookId

from .replicator import Replicator

from .listener import EventListener
from .listener import TerminateListener

from .unotool import getDesktop
from .unotool import getUrl

from .dbtool import getSqlException

from .logger import logMessage
from .logger import getMessage
g_message = 'datasource'

from .configuration import g_scheme

import traceback


class DataSource(unohelper.Base,
                 XRestDataSource):
    def __init__(self, ctx):
        self._ctx = ctx
        self._count = 0
        self._users = {}
        self._addressbooks = {}
        self._listener = EventListener(self)
        #self._provider = Provider(ctx)
        self._database = DataBase(ctx)
        #self._replicator = Replicator(ctx, self._database, self._provider, self._connections)
        #listener = TerminateListener(self._replicator)
        #desktop = getDesktop(ctx)
        #desktop.addTerminateListener(listener)

# XRestDataSource
    def getConnection(self, user, password):
        connection = self._database.getConnection(user, password)
        connection.addEventListener(self._listener)
        self._count += 1
        return connection

    def stopReplicator(self):
        if self._count > 0:
            self._count -= 1
        print("DataSource.disposeConnection() %s" % self._count)
        if self._count == 0:
            #self._replicator.stop()
            pass

    def getDataBaseCredential(self, url, name, password):
        scheme, server, addressbook = self._getUrlParts(url)
        if not server:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % url)
        print("DataSource.getDataBaseCredential() 1 %s - %s - %s" % (scheme, server, addressbook))
        uid = getUserId(server, name)
        aid = getAddressbookId(uid, addressbook)
        if aid in self._addressbooks:
            name, password = self._addressbooks.get(aid).getDataBaseCredential()
        else:
            if uid in self._users:
                u = self._users.get(uid)
            else:
                u = User(self._ctx, self._database, scheme, server, name, password)
                self._users[uid] = u
            a = AddressBook(self._ctx, self._database, u, addressbook)
            self._addressbooks[aid] = a
            name, password = a.getDataBaseCredential()
            if aid != name:
                self._addressbooks[name] = a
        # User and/or AddressBook has been initialized and the connection to the database is done...
        # We can start the database replication in a background task.
        #self._replicator.start()
        return name, password

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location, g_scheme)
        if url is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % location)
        scheme = url.Protocol if url.Protocol else g_scheme
        server = url.Server
        addressbook = url.Path.strip('/')
        if scheme + server + addressbook != location:
            scheme = g_scheme
        return scheme, server, addressbook

    def _getSqlException(self, state, code, format):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, format)
        error = getSqlException(state, code, msg, self)
        return error
