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

from com.sun.star.rest import XDataParser

from .unolib import KeyMap
from .unotool import getNamedValue

from collections import OrderedDict
import xml.etree.ElementTree as XmlTree


class DataParser(unohelper.Base,
                 XDataParser):
    def __init__(self, method, predicate=None):
        #self._provider = provider
        #self.map = database.getFieldsMap(method, True)
        #self.keys = self.map.getKeys()
        self._method = method
        self._predicate = predicate
        self._path = None
        self._root = None
        self._keys = self._getKeys()

    def parse(self, response):
        root = XmlTree.fromstring(response)
        print("DataParser.parseResponse() 1 %s" % root.tag)
        print("DataParser.parseResponse() 2\n%s" % response)
        print("DataParser.parseResponse() 3\n%s" % XmlTree.tostring(root))
        if self._path is None:
            data = self._parseResponse(root, self._keys)
        else:
            data = self._parseMultiResponse(root)
        return data

    def _parseResponse(self, root, keys, first=True):
        data = self._getData(first)
        return self._parseItem(data, root, keys, first)

    def _parseItem(self, data, root, keys, first=True):
        print("DataParser._parseItem() 1")
        for key, method in keys.items():
            path, attribut = method
            value = None
            print("DataParser._parseItem() 2 %s" % path)
            item = root.find(path)
            print("DataParser._parseItem() 3 %s" % item)
            if item is not None:
                value = item.text if attribut is None else item.get(attribut)
            print("DataParser._parseItem() 4 %s" % value)
            data = self._setData(data, key, value, first)
        return data

    def _parseMultiResponse(self, root):
        data = self._getData(True)
        print("DataParser._parseMultiResponse() 1 %s" % (data, ))
        for item in root.findall(self._path):
            if self._root is None:
                value = self._parseResponse(item, self._keys, False)
                data = self._setData(data, None, value, True)
            else:
                data = self._parseItem(data, item, self._keys)
            print("DataParser._parseMultiResponse() 2 %s" % (data, ))
        if self._root is not None:
            data = self._parseItem(data, root, self._root)
            print("DataParser._parseMultiResponse() 3 %s" % (data, ))
            data = self._setData(None, None, data)
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
        elif self._method == 'getDefaultAddressbook':
            keys = OrderedDict()
            path = './{DAV:}response[2]/'
            keys['Url'] = (path + '{DAV:}href', None)
            path += '{DAV:}propstat/{DAV:}prop/'
            keys['Name'] = (path + '{DAV:}displayname', None)
            item = '{http://calendarserver.org/ns/}getctag'
            keys['Tag'] = (path + item, None)
            keys['Token'] = (path + '{DAV:}sync-token', None)
        elif self._method == 'getAllAddressbook':
            keys = OrderedDict()
            path = "./{DAV:}propstat/{DAV:}status[.='HTTP/1.1 200 OK']"
            # FIXME: Name is the fist property:
            # FIXME: We need to exclude Addressbook without first property
            keys['Name'] = (path + '../{DAV:}prop/{DAV:}displayname', None)
            keys['Url'] = (path + '..../{DAV:}href', None)
            item = '../{DAV:}prop/{http://calendarserver.org/ns/}getctag'
            keys['Tag'] = (path + item, None)
            keys['Token'] = (path + '../{DAV:}prop/{DAV:}sync-token', None)
            self._path = './{DAV:}response'
        elif self._method == 'getAddressbookUrl':
            keys = OrderedDict()
            if not self._predicate:
                path = './{DAV:}response[2]/'
            else:
                path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../" % self._predicate
            keys['Url'] = (path + '{DAV:}href', None)
            path += '{DAV:}propstat/{DAV:}prop/'
            keys['Name'] = (path + '{DAV:}displayname', None)
            item = '{http://calendarserver.org/ns/}getctag'
            keys['Tag'] = (path + item, None)
            keys['Token'] = (path + '{DAV:}sync-token', None)
        elif self._method == 'getAddressbook':
            keys = {}
            path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../{DAV:}href" % self._predicate
            keys['Url'] = (path, None)
        elif self._method == 'getAddressbookCards':
            keys = OrderedDict()
            keys['Url'] = ('./{DAV:}href', None)
            path = './{DAV:}propstat/{DAV:}prop/%s'
            keys['Tag'] = (path % '{DAV:}getetag', None)
            item = '{urn:ietf:params:xml:ns:carddav}address-data'
            keys['Data'] = (path % item, None)
            self._path = './{DAV:}response'
        elif self._method == 'getModifiedCardByToken':
            keys = OrderedDict()
            path = "./{DAV:}propstat/{DAV:}status[.='HTTP/1.1 200 OK']..../{DAV:}href"
            keys['Modified'] = (path, None)
            path = "./{DAV:}status[.='HTTP/1.1 404 Not Found']../{DAV:}href"
            keys['Deleted'] = (path, None)
            self._path = './{DAV:}response'
            self._root = {'Token': ('./{DAV:}sync-token', None)}
        return keys

    def _getData(self, first=True):
        if self._method == 'getUrl':
            data = KeyMap()
        elif self._method == 'getUser':
            data = None
        elif self._method == 'getAddressbooksUrl':
            data = None
        elif self._method == 'getDefaultAddressbook':
            data = []
        elif self._method == 'getAllAddressbook':
            data = [] if first else KeyMap()
        elif self._method == 'getAddressbookUrl':
            data = []
        elif self._method == 'getAddressbook':
            data = None
        elif self._method == 'getAddressbookCards':
            data = []
        elif self._method == 'getModifiedCardByToken':
            data = {'Token': None, 'Modified': [], 'Deleted': []}
        return data

    def _setData(self, data, key, value, first=True):
        if self._method == 'getUrl':
            data.insertValue(key, value)
        elif self._method == 'getUser':
            data = value
        elif self._method == 'getAddressbooksUrl':
            data = value
        elif self._method == 'getDefaultAddressbook':
            data.append(value)
        elif self._method == 'getAllAddressbook':
            # FIXME: We need to exclude Addressbook without first property: Name
            if value is not None:
                if not first:
                    data.setValue(key, value)
                elif value.getKeys() == self._keys:
                    data.append(value)
        elif self._method == 'getAddressbookUrl':
            data.append(value)
        elif self._method == 'getAddressbook':
            data = value
        elif self._method == 'getAddressbookCards':
            data.append(value)
        elif self._method == 'getModifiedCardByToken':
            if key is None:
                data = value['Token'], value['Modified'], value['Deleted']
            elif key == 'Token':
                data['Token'] = value
            elif value is not None:
                data[key].append(value)
        return data





class DataIterator(unohelper.Base,
                   XDataParser):
    def __init__(self, method, addressbook=None):
        #self._provider = provider
        #self.map = database.getFieldsMap(method, True)
        #self.keys = self.map.getKeys()
        self.DataType = 'Xml'
        self._method = method
        self._addressbook = addressbook
        self._path = None
        self._keys = self._getKeys()
        self._ns = {'': 'DAV:',
                    'card': 'urn:ietf:params:xml:ns:carddav'}

    def parse(self, response):
        root = XmlTree.fromstring(response)
        print("DataParser.parseResponse() 1 %s" % root.tag)
        print("DataParser.parseResponse() 2\n%s" % response)
        print("DataParser.parseResponse() 3\n%s" % XmlTree.tostring(root))
        if self._path is None:
            data = self._parseResponse(root)
        else:
            data = self._parseMultiResponse(root)
        return data

    def _parseResponse(self, root):
        data = self._getData()
        for key, method in self._keys.items():
            print("DataParser._parseUniqueResponse() 1 %s" % key)
            path, attribut = method
            value = None
            item = root.find(path)
            if item is not None:
                value = item.text if attribut is None else item.get(attribut)
            print("DataParser._parseUniqueResponse() 2 %s" % value)
            data = self._setData(data, key, value)
        return data

    def _parseMultiResponse(self, root):
        data = self._getData()
        for item in root.findall(self._path):
            value = self._parseResponse(item)
            print("DataParser._parseMultiResponse() 1 %s" % (value, ))
            data = self._setData(data, None, value)
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
        elif self._method == 'getDefaultAddressbook':
            keys = OrderedDict()
            path = './{DAV:}response[2]/'
            keys['Url'] = (path + '{DAV:}href', None)
            path += '{DAV:}propstat/{DAV:}prop/'
            keys['Name'] = (path + '{DAV:}displayname', None)
            item = '{http://calendarserver.org/ns/}getctag'
            keys['Tag'] = (path + item, None)
            keys['Token'] = (path + '{DAV:}sync-token', None)
        elif self._method == 'getAddressbookUrl':
            keys = OrderedDict()
            if not self._addressbook:
                path = './{DAV:}response[2]/'
            else:
                path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../" % self._addressbook
            keys['Url'] = (path + '{DAV:}href', None)
            path += '{DAV:}propstat/{DAV:}prop/'
            keys['Name'] = (path + '{DAV:}displayname', None)
            item = '{http://calendarserver.org/ns/}getctag'
            keys['Tag'] = (path + item, None)
            keys['Token'] = (path + '{DAV:}sync-token', None)
        elif self._method == 'getAddressbook':
            keys = {}
            path = ".//*{DAV:}prop[{DAV:}displayname='%s']..../{DAV:}href" % self._addressbook
            keys['Url'] = (path, None)
        elif self._method == 'getAddressbookCards':
            keys = OrderedDict()
            keys['Url'] = ('./{DAV:}href', None)
            path = './{DAV:}propstat/{DAV:}prop/%s'
            keys['Etag'] = (path % '{DAV:}getetag', None)
            item = '{urn:ietf:params:xml:ns:carddav}address-data'
            keys['Data'] = (path % item, None)
            self._path = './{DAV:}response'
        return keys

    def _getData(self):
        if self._method == 'getUrl':
            data = KeyMap()
        elif self._method == 'getUser':
            data = None
        elif self._method == 'getAddressbooksUrl':
            data = None
        elif self._method == 'getDefaultAddressbook':
            data = []
        elif self._method == 'getAddressbookUrl':
            data = []
        elif self._method == 'getAddressbook':
            data = None
        elif self._method == 'getAddressbookCards':
            data = []
        return data

    def _setData(self, data, key, value):
        if self._method == 'getUrl':
            data.insertValue(key, value)
        elif self._method == 'getUser':
            data = value
        elif self._method == 'getAddressbooksUrl':
            data = value
        elif self._method == 'getDefaultAddressbook':
            data.append(value)
        elif self._method == 'getAddressbookUrl':
            data.append(value)
        elif self._method == 'getAddressbook':
            data = value
        elif self._method == 'getAddressbookCards':
            data.append(value)
        return data
