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

from com.sun.star.ucb.ConnectionMode import OFFLINE
from com.sun.star.ucb.ConnectionMode import ONLINE

from .addressbook import AddressBooks

from .provider import Provider

from .oauth2lib import getRequest
from .oauth2lib import g_oauth2

from .unotool import executeDispatch

from .dbtool import getSqlException

from .dbconfig import g_user
from .dbconfig import g_schema

from .logger import getMessage
g_message = 'datasource'

import traceback


def getUserUri(server, name):
    return server + '/' + name


class User(unohelper.Base):
    def __init__(self, ctx, database, scheme, server, name, pwd=''):
        self._ctx = ctx
        self._password = pwd
        self._request = getRequest(ctx, server, name)
        self._metadata = database.selectUser(server, name)
        self._sessions = []
        if self._isNewUser():
            provider = Provider(ctx, scheme, server)
            self._metadata = self._getNewUser(database, provider, scheme, server, name, pwd)
            self.createUser(database)
        else:
            provider = Provider(ctx, self.Scheme, self.Server)
        self._provider = provider
        self._addressbooks = AddressBooks(ctx, self._metadata)

    @property
    def Id(self):
        return self._metadata.getValue('User')
    @property
    def Scheme(self):
        return self._metadata.getValue('Scheme')
    @property
    def Server(self):
        return self._metadata.getValue('Server')
    @property
    def Path(self):
        return self._metadata.getValue('Path')
    @property
    def Name(self):
        return self._metadata.getValue('Name')
    @property
    def Password(self):
        return self._password
    @property
    def Addressbooks(self):
        return self._addressbooks

# Procedures called by DataSource
    def getUri(self):
        return getUserUri(self.Server, self.Name)

    def getName(self):
        return g_user % self.Id

    def getSchema(self):
        return g_schema % self.Id

    def getPassword(self):
        password = ''
        return password

    def hasSession(self):
        return len(self._sessions) > 0

    def addSession(self, session):
        self._sessions.append(session)

    def removeSession(self, session):
        if session in self._sessions:
            self._sessions.remove(session)

    def initAddressbooks(self, database):
        if self._provider.isOnLine():
            addressbooks = self._provider.getAllAddressbook(self._request, self.Name, self.Password, self.Path)
            if not addressbooks:
                #TODO: Raise SqlException with correct message!
                print("User.initAddressbooks() 1 %s" % (addressbooks, ))
                raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % self.User.Server)
            if self._addressbooks.initAddressbooks(database, self.Id, addressbooks):
                database.initAddressbooks()

    def unquoteUrl(self, url):
        return self._request.unquoteUrl(url)

    def addAddressbook(self, aid):
        pass
        #if aid not in self._addressbooks:
        #    self._addressbooks.append(aid)

    def removeAddressbook(self, aid):
        pass
        #if aid in self._addressbooks:
        #    print("User.removeAddressbook() 1 %s" % (self._addressbooks, ))
        #    self._addressbooks.remove(aid)

    def getAddressbooks(self):
        return self._addressbooks.getAddressbooks()

    def createUser(self, database):
        name = self.getName()
        if not database.createUser(name, self.getPassword()):
            raise self._getSqlException(1005, 1106, name)
        database.createUserSchema(self.getSchema(), name)

    def isOffLine(self):
        return self._provider.isOffLine()

    def getAddressbookUrl(self, name):
        return self._provider.getAddressbookUrl(self._request, name, self.Name, self.Password, self.Path)

    def getAddressbook(self, name, path):
        return self._provider.getAddressbook(self._request, name, self.Name, self.Password, path)

    def getAddressbookCards(self, path):
        return self._provider.getAddressbookCards(self._request, self.Name, self.Password, path)

    def getModifiedCardByToken(self, path, token):
        return self._provider.getModifiedCardByToken(self._request, self.Name, self.Password, path, token)

    def getModifiedCard(self, path, urls):
        return self._provider.getModifiedCard(self._request, self.Name, self.Password, path, urls)

    def _isNewUser(self):
        return self._metadata is None

    def _getNewUser(self, database, provider, scheme, server, user, pwd):
        if self._request is None:
            raise self._getSqlException(1003, 1105, g_oauth2)
        if provider.isOffLine():
            raise self._getSqlException(1004, 1108, user)
        url = provider.getWellKnownUrl()
        redirect, url = provider.getDiscoveryUrl(self._request, user, pwd, url)
        print("User._getMetaData() 1 %s" % url)
        if redirect:
            scheme, server = provider.getUrlParts(url)
            redirect, url = provider.getDiscoveryUrl(self._request, user, pwd, url)
        path = provider.getUserUrl(self._request, user, pwd, url)
        if path is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, 'Server: %s Bad password: %s!' % (self.User.Server, pwd))
        if not provider.supportAddressbook(self._request, user, pwd, path):
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % server)
        print("User._getMetaData() 2 %s" % path)
        path = provider.getAddressbooksUrl(self._request, user, pwd, path)
        print("User._getMetaData() 3 %s" % path)
        if path is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, 'Server: %s Bad password: %s!' % (self.User.Server, pwd))
        return database.insertUser(scheme, server, path, user)

    def _getSqlException(self, state, code, format):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, format)
        error = getSqlException(state, code, msg, self)
        return error
