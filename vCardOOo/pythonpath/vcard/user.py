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

from com.sun.star.sdbc import XRestUser

from .provider import Provider

from .oauth2lib import getRequest
from .oauth2lib import g_oauth2

from .unotool import executeDispatch
from .unotool import getUrl

from .dbtool import getSqlException

from .logger import getMessage
g_message = 'datasource'

from .configuration import g_scheme

import traceback


class User(unohelper.Base,
           XRestUser):
    def __init__(self, ctx, database, url, name, password=''):
        self._ctx = ctx
        #self.Fields = database.getUserFields()
        #url = 'gcontact:request'
        #executeDispatch(ctx, url)
        scheme, server, addressbook = self._getUrlParts(url)
        print("User.__init__() 1 %s - %s - %s" % (scheme, server, addressbook))
        if not server:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % url)
        self._provider = Provider(ctx, scheme, server)
        self._request = getRequest(ctx, server, name)
        self._metadata = database.selectUser(addressbook, server, name)
        if self._isNew():
            self._metadata = self._getMetaData(database, server, addressbook, name, password)
            self._initUser(database, password)

    @property
    def User(self):
        return self._metadata.getDefaultValue('User', None)
    @property
    def Addressbook(self):
        return self._metadata.getDefaultValue('Addressbook', None)
    @property
    def Group(self):
        return self._metadata.getDefaultValue('Group', None)
    @property
    def Scheme(self):
        return self._metadata.getDefaultValue('Scheme', '')
    @property
    def Server(self):
        return self._metadata.getDefaultValue('Server', '')
    @property
    def Path(self):
        return self._metadata.getDefaultValue('Path', '')
    @property
    def Name(self):
        return self._metadata.getDefaultValue('UserName', '')
    @property
    def Password(self):
        return self._metadata.getDefaultValue('Password', '')
    @property
    def AddressbookName(self):
        return self._metadata.getDefaultValue('AddressbookName', '')
    @property
    def Async(self):
        return self._metadata.getDefaultValue('Async', None)
    @property
    def Gsync(self):
        return self._metadata.getDefaultValue('Gsync', None)

    def _getUrlParts(self, location)
        url = getUrl(self._ctx, location)
        if location is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % location)
        scheme = url.Protocol if url.Protocol else g_scheme
        server = url.Server
        addressbook = url.Path.strip('/')
        return scheme, server, addressbook

    def _isNew(self):
        return self._metadata is None

    def _getMetaData(self, database, server, addressbook, user, password):
        if self._request is None:
            raise self._getSqlException(1003, 1105, g_oauth2)
        if self._provider.isOffLine():
            raise self._getSqlException(1004, 1108, user)
        location = self._provider.getDiscoveryLocation(self._request, server, user, password)
        print("User._getMetaData() 1 %s" % location)
        url = self._provider.getUserUrl(self._request, user, password, location)
        if not self._provider.hasAddressbook(self._request, user, password, url):
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % server)
        print("User._getMetaData() 2 %s" % url)
        url = self._provider.getAddressbooksUrl(self._request, user, password, url)
        print("User._getMetaData() 3 %s" % url)
        url, addressbook = self._provider.getAddressbookUrl(self._request, addressbook, user, password, url)
        if url is None or addressbook is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % server)
        print("User._getMetaData() 4 %s - %s" % (url, addressbook))
        if not self._provider.getAddressbook(self._request, addressbook, user, password, url):
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % server)
        print("User._getMetaData() 5 %s" % url)
        return database.insertUser(server, addressbook, url, user, password)

    def _initUser(self, database, password):
        credential = self._getCredential(password)
        if not database.createUser(*credential):
            raise self._getSqlException(1005, 1106, name)
        format = {'Schema': self.User,
                  'Server': self.Server,
                  'User': self.Name,
                  'Group': self.Group}
        database.initUser(format)

    def _getCredential(self, password):
        return self.Name, password

    def _getSqlException(self, state, code, format):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, format)
        error = getSqlException(state, code, msg, self)
        return error
