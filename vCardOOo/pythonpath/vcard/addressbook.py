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

from .dbtool import getSqlException

from .logger import getMessage
g_message = 'datasource'

import traceback


class AddressBook(unohelper.Base):
    def __init__(self, ctx, database, user, aid=None, name=''):
        self._ctx = ctx
        print("AddressBook.__init__() 1 %s - %s - %s" % (user.Scheme, user.Server, name))
        self.User = user
        name = self.User.unquoteUrl(name)
        self._metadata = database.selectAddressbook(user.Id, aid, name)
        print("AddressBook.__init__() 2 %s - '%s' - %s" % (user.Id, name, self._metadata))
        if self._isNewAddressbook():
            self._metadata = self._getNewAddressbook(database, name)
            self.User.createAddressbook(database, self.Name, self.Id)
        if aid is None:
            self.User.addAddressbook(self.Id)

    @property
    def Id(self):
        return self._metadata.getValue('Addressbook')
    @property
    def Group(self):
        return self._metadata.getValue('Group')
    @property
    def Path(self):
        return self._metadata.getValue('Path')
    @property
    def Name(self):
        return self._metadata.getValue('Name')
    @property
    def Tag(self):
        return self._metadata.getValue('Tag')
    @property
    def AdrSync(self):
        return self._metadata.getValue('AdrSync')
    @property
    def GrpSync(self):
        return self._metadata.getValue('GrpSync')
    @property
    def New(self):
        return self._metadata.getValue('New')

    def getDataBaseCredential(self):
        return self.User.getDataBaseCredential(self.Id)

    def getAddressbookCards(self):
        return self.User.getAddressbookCards(self.Path)

    def getModifiedCardByToken(self):
        return self.User.getModifiedCardByToken(self.Path, self.AdrSync)

    def getModifiedCard(self, urls):
        return self.User.getModifiedCard(self.Path, urls)

    def _isNewAddressbook(self):
        return self._metadata is None

    def _getNewAddressbook(self, database, name):
        if self.User.isOffLine():
            raise self._getSqlException(1004, 1108, self.User.Name)
        path, name, tag, token = self.User.getAddressbookUrl(name)
        if path is None or name is None:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % self.User.Server)
        print("AddressBook._getMetaData() 1 %s - %s" % (path, name))
        if not self.User.getAddressbook(name, path):
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1004, 1108, '%s has no support of CardDAV!' % self.User.Server)
        print("AddressBook._getMetaData() 2 %s" % path)
        keymap = database.insertAddressbook(self.User.Id, path, name, tag, token)
        print("AddressBook._getMetaData() 3 %s" % name)
        i = 4
        for key in keymap.getKeys():
            print("AddressBook._getMetaData() %i %s - %s" % (i, key, keymap.getValue(key)))
            i += 1
        return keymap

    def getAddressbookId(self):
        return '%i' % self.Id

    def _getSqlException(self, state, code, format):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, format)
        error = getSqlException(state, code, msg, self)
        return error
