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

from com.sun.star.auth import XRestDataParser

from .unolib import KeyMap
from .unotool import getNamedValue

from collections import OrderedDict
import xml.etree.ElementTree as XmlTree


class DataParser(unohelper.Base,
                 XRestDataParser):
    def __init__(self, method, addressbook=None):
        #self._provider = provider
        #self.map = database.getFieldsMap(method, True)
        #self.keys = self.map.getKeys()
        self.DataType = 'Xml'
        self._method = method
        self._addressbook = addressbook
        self._keys = self._getKeys()
        self._ns = {'': 'DAV:',
                    'card': 'urn:ietf:params:xml:ns:carddav'}

    def parseResponse(self, response):
        data = self._getData()
        root = XmlTree.fromstring(response)
        print("DataParser.parseResponse() 1 %s" % root.tag)
        print("DataParser.parseResponse() 2\n%s" % response)
        print("DataParser.parseResponse() 3\n%s" % XmlTree.tostring(root))
        for key, method in self._keys.items():
            path, attribut = method
            value = None
            item = root.find(path)
            if item is not None:
                value = item.text if attribut is None else item.get(attribut)
            print("DataParser.parseResponse() 4 %s" % value)
            data = self._setData(data, key, value)
        return data

    def _getKeys(self):
        if self._method == 'getUrl':
            keys = OrderedDict()
            keys['Url'] = ('./{DAV:}response/{DAV:}href', None)
        elif self._method == 'getUser':
            keys = {}
            item = '{DAV:}current-user-principal'
            path = './{DAV:}response/{DAV:}propstat/{DAV:}prop/%s/{DAV:}href'
            keys['Url'] = (path % item, None)
        elif self._method == 'getAddressbooksUrl':
            keys = {}
            item = '{urn:ietf:params:xml:ns:carddav}addressbook-home-set'
            path = './{DAV:}response/{DAV:}propstat/{DAV:}prop/%s/{DAV:}href'
            keys['Url'] = (path % item, None)
        elif self._method == 'getAddressbookUrl':
            keys = {}
            if not self._addressbook:
                path = './{DAV:}response[2]/'
            else:
                path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../" % self._addressbook
            keys['Url'] = (path + '{DAV:}href', None)
            path += '{DAV:}propstat/{DAV:}prop/{DAV:}displayname'
            keys['Name'] = (path, None)
        elif self._method == 'getAddressbook':
            keys = {}
            path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../{DAV:}href" % self._addressbook
            keys['Url'] = (path, None)
        return keys

    def _getData(self):
        if self._method == 'getUrl':
            data = KeyMap()
        elif self._method == 'getUser':
            data = None
        elif self._method == 'getAddressbooksUrl':
            data = None
        elif self._method == 'getAddressbookUrl':
            data = []
        elif self._method == 'getAddressbook':
            data = None
        return data

    def _setData(self, data, key, value):
        if self._method == 'getUrl':
            data.insertValue(key, value)
        elif self._method == 'getUser':
            data = value
        elif self._method == 'getAddressbooksUrl':
            data = value
        elif self._method == 'getAddressbookUrl':
            data.append(value)
        elif self._method == 'getAddressbook':
            data = value
        return data
