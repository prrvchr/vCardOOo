#!
# -*- coding: utf-8 -*-

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

from collections import OrderedDict
import traceback


class AddressBooks(unohelper.Base):
    def __init__(self, ctx, metadata):
        self._ctx = ctx
        print("AddressBooks.__init__() 1")
        self._addressbooks = self._getAddressbooks(metadata)
        print("AddressBooks.__init__() 2")

    def initAddressbooks(self, database, user, addressbooks):
        print("AddressBooks.initAddressbooks() 1")
        changed = False
        for name, url, tag, token in addressbooks:
            if not self._hasAddressbook(url):
                index = database.insertAddressbook(user, url, name, tag, token)
                addressbook = AddressBook(self._ctx, index, url, name, tag, token, True)
                self._addressbooks[url] = addressbook
                changed = True
                print("AddressBooks.initAddressbooks() 2 %s - %s - %s" % (index, name, url))
            else:
                addressbook = self._getAddressbook(url)
                if addressbook.hasNameChanged(name):
                    database.updateAddressbookName(addressbook.Id, name)
                    addressbook.setName(name)
                    changed = True
                    print("AddressBooks.initAddressbooks() 3 %s" % (name, ))
        print("AddressBooks.initAddressbooks() 4")
        return changed
            
    def getAddressbooks(self):
        return self._addressbooks.values()

    def _hasAddressbook(self, url):
        return url in self._addressbooks

    def _getAddressbook(self, url):
        return self._addressbooks[url]

    def _getAddressbooks(self, metadata):
        addressbooks = OrderedDict()
        indexes = metadata.getValue('Addressbooks')
        names = metadata.getValue('Names')
        tags = metadata.getValue('Tags')
        tokens = metadata.getValue('Tokens')
        i = 0
        for url in metadata.getValue('Paths'):
            addressbooks[url] = AddressBook(self._ctx, indexes[i], url, names[i], tags[i], tokens[i])
            i += 1
        return addressbooks


class AddressBook(unohelper.Base):
    def __init__(self, ctx, index, url, name, tag, token, new=False):
        self._ctx = ctx
        self._index = index
        self._url = url
        self._name = name
        self._tag = tag
        self._token = token
        self._new = new

    @property
    def Id(self):
        return self._index
    @property
    def Path(self):
        return self._url
    @property
    def Name(self):
        return self._name
    @property
    def Tag(self):
        return self._tag
    @property
    def Token(self):
        return self._token

    def isNew(self):
        new = self._new
        self._new = False
        return new

    def hasNameChanged(self, name):
        return self.Name != name

    def setName(self, name):
        self.Name = name

    def _getSqlException(self, state, code, *args):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, args)
        error = getSqlException(state, code, msg, self)
        return error
