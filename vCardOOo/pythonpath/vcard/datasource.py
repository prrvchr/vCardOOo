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


from .configuration import g_identifier
from .configuration import g_group
from .configuration import g_compact

from .database import DataBase

from .user import User
from .user import getUserId

from .addressbook import AddressBook

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


class DataSource(unohelper.Base):
    def __init__(self, ctx):
        self._ctx = ctx
        self._count = 0
        self._users = {}
        self._listener = EventListener(self)
        self._database = DataBase(ctx)
        self._replicator = Replicator(ctx, self._database, self._users)
        listener = TerminateListener(self._replicator)
        getDesktop(ctx).addTerminateListener(listener)

# XRestDataSource
    def getConnection(self, user, password):
        connection = self._database.getConnection(user, password)
        connection.addEventListener(self._listener)
        self._count += 1
        return connection

    def closeConnection(self, connection):
        url = connection.getMetaData().getUserName()
        server, name, aid = self._getUrlParts(url)
        uid = getUserId(server, name)
        if uid in self._users:
            self._users.get(uid).removeAddressbook(aid)
        if self._count > 0:
            self._count -= 1
        print("DataSource.closeConnection() 1: %s - %s - %s - %s" % (self._count, server, name, aid))
        if self._count == 0:
            #self._replicator.stop()
            pass

    def getConnectionCredential(self, scheme, server, addressbook, name, password):
        print("DataSource.getDataBaseCredential() 1 %s - %s - %s" % (scheme, server, addressbook))
        uid = getUserId(server, name)
        if uid in self._users:
            user = self._users.get(uid)
        else:
            user = User(self._ctx, self._database, scheme, server, name, password)
            self._users[uid] = user
        a = AddressBook(self._ctx, self._database, user, None, addressbook)
        name, password = a.getDataBaseCredential()
        # User and/or AddressBook has been initialized and the connection to the database is done...
        # We can start the database replication in a background task.
        self._replicator.start()
        return name, password

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location, g_scheme)
        server = url.Server
        user = url.Path.strip('/')
        aid = int(url.Name)
        return server, user, aid

