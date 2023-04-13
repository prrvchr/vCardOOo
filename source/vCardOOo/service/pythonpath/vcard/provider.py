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

from .unolib import KeyMap

from .unotool import getUrl

from .providerbase import ProviderBase

import xml.etree.ElementTree as ET
import traceback


class Provider(ProviderBase):
    def __init__(self, ctx, scheme, server):
        self._ctx = ctx
        self._length = 256
        self._scheme = scheme
        self._server = server
        self._url = '/.well-known/carddav'
        self._headers = ('1', 'access-control', 'addressbook')
        self._status = 'HTTP/1.1 404 Not Found'

    def insertUser(self, database, request, scheme, server, name, pwd):
        userid = self._getNewUserId(request, server, name, pwd)
        return database.insertUser(scheme, server, userid, name)

    def _getNewUserId(self, request, server, name, pwd):
        try:
            url = self._scheme + self._server + self._url
            redirect, url = self._getDiscoveryUrl(request, name, pwd, url)
            print("Provider.getNewUserId() 1 Redirect: %s - Url: %s" % (redirect, url))
            if redirect:
                scheme, server = self._getUrlParts(url)
                redirect, url = self._getDiscoveryUrl(request, name, pwd, url)
                print("Provider.getNewUserId() 2 Redirect: %s - Url: %s" % (redirect, url))
            path = self._getUserUrl(request, name, pwd, url)
            print("Provider.getNewUserId() 3 Path: %s" % (path, ))
            if path is None:
                #TODO: Raise SqlException with correct message!
                raise self.getSqlException(1004, 1108, 'getNewUserId', 'Server: %s Bad password: %s!' % (server, '*'*pwd))
            if not self._supportAddressbook(request, name, pwd, path):
                #TODO: Raise SqlException with correct message!
                raise self.getSqlException(1004, 1108, 'getNewUserId', '%s has no support of CardDAV!' % server)
            print("Provider.getNewUserId() 4 %s" % path)
            userid = self._getAddressbooksUrl(request, name, pwd, path)
            print("Provider.getNewUserId() 5 %s" % userid)
            if userid is None:
                #TODO: Raise SqlException with correct message!
                raise self.getSqlException(1004, 1108, 'getNewUserId', 'Server: %s Bad password: %s!' % (server, '*'*pwd))
            return userid
        except Exception as e:
            msg = "Provider.getNewUserId() Error: %s" % traceback.format_exc()
            print(msg)

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location)
        self._scheme = url.Protocol
        self._server = url.Server
        return self._scheme, self._server

    def _getDiscoveryUrl(self, request, name, password, url):
        parameter = self._getRequestParameter('getUrl', name, password, url)
        response = request.executeRequest(parameter)
        if not response.Ok or not response.IsRedirect:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getDiscoveryUrl()', '%s Response not Ok' % url)
        location = response.getHeader('Location')
        response.close()
        if not location:
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getDiscoveryUrl()', '%s url is None' % url)
        redirect = location.endswith(self._url)
        return redirect, location

    def _getUserUrl(self, request, name, password, url):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:current-user-principal />
  </d:prop>
</d:propfind>
'''
        parameter = self._getRequestParameter('getUser', name, password, url, data)
        response = request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            raise self.getSqlException(1006, 1107, 'getUserUrl()', name)
        url = self._parseUserUrl(response)
        response.close()
        return url

    def _parseUserUrl(self, response):
        url = None
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._length, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag != '{DAV:}current-user-principal':
                    continue
                for child in element:
                    if child.tag == '{DAV:}href' and child.text:
                        url = child.text
                        break
            # FIXME: We got what we wanted we can leave
            if url is not None:
                break
        return url

    def _supportAddressbook(self, request, user, password, url):
        parameter = self._getRequestParameter('hasAddressbook', user, password, url)
        response = request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'supportAddressbook()', user)
        headers = response.getHeader('DAV')
        response.close()
        for headers in self._headers:
            if headers not in headers:
                return False
        return True

    def _getAddressbooksUrl(self, request, name, pwd, url):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <card:addressbook-home-set />
  </d:prop>
</d:propfind>
'''
        parameter = self._getRequestParameter('getAddressbooksUrl', name, pwd, url, data)
        response = request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            raise self.getSqlException(1006, 1107, 'getAddressbooksUrl()', name)
        url = self._parseAddressbookUrl(response)
        response.close()
        return url

    def _parseAddressbookUrl(self, response):
        url = None
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._length, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag != '{urn:ietf:params:xml:ns:carddav}addressbook-home-set':
                    continue
                for child in element:
                    if child.tag == '{DAV:}href' and child.text:
                        url = child.text
                        break
            # FIXME: We got what we wanted we can leave
            if url is not None:
                break
        return url

    def initAddressbooks(self, database, user):
        if self.isOnLine():
            addressbooks = self._getAllAddressbook(user)
            if not addressbooks:
                #TODO: Raise SqlException with correct message!
                print("User.initAddressbooks() 1 %s" % (addressbooks, ))
                raise self.getSqlException(1004, 1108, 'initAddressbooks', '%s has no support of CardDAV!' % user.Server)
            if user.Addressbooks.initAddressbooks(database, user.Id, addressbooks):
                database.initAddressbooks(user)

    def _getAllAddressbook(self, user):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav" xmlns:cs="http://calendarserver.org/ns/">
  <d:prop>
    <d:displayname />
    <cs:getctag />
    <d:sync-token />
    <d:resourcetype>
        <card:addressbook />
    </d:resourcetype>
  </d:prop>
</d:propfind>
'''
        parameter = self._getRequestParameter('getAllAddressbook', user.Name, user.Password, user.Path, data)
        response = user.Request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getAllAddressbook()', user.Name)
        addressbooks = []
        for addressbook in self._parseAllAddressbook(response):
            addressbooks.append(addressbook)
        response.close()
        return addressbooks

    def _parseAllAddressbook(self, response):
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._length, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag != '{DAV:}response':
                    continue
                url = name = token = tag = None
                for child in element.iter():
                    if child.tag == '{DAV:}href' and child.text:
                        url = child.text
                    elif child.tag == '{DAV:}displayname' and child.text:
                        name = child.text
                    elif child.tag == '{DAV:}sync-token' and child.text:
                        token = child.text
                    elif child.tag == '{http://calendarserver.org/ns/}getctag' and child.text:
                        tag = child.text
                if all((url, name, token, tag)):
                    yield KeyMap(**{'Url': url, 'Name': name, 'Token': token, 'Tag': tag})

    def firstCardPull(self, database, user, addressbook):
        data = '''\
<?xml version="1.0"?>
<card:addressbook-query xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <d:getetag />
    <card:address-data />
  </d:prop>
</card:addressbook-query>
'''
        parameter = self._getRequestParameter('getAddressbookCards', user.Name, user.Password, addressbook.Path, data)
        response = user.Request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getAddressbookCards()', user)
        count = database.mergeCard(addressbook.Id, self._parseCards(response))
        response.close()
        return count

    def getCardByToken(self, user, addressbook):
        data = '''\
<?xml version="1.0"?>
<d:sync-collection xmlns:d="DAV:">
  <d:sync-token>%s</d:sync-token>
  <d:sync-level>1</d:sync-level>
  <d:prop>
    <d:getetag />
  </d:prop>
</d:sync-collection>
''' % addressbook.Token
        parameter = self._getRequestParameter('getModifiedCardByToken', user.Name, user.Password, addressbook.Path, data)
        response = user.Request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getModifiedCardByToken()', user.Name)
        token, deleted, modified = self._getChangedCards(response)
        response.close()
        return token, deleted, modified

    def mergeCardByToken(self, database, user, addressbook, urls):
        data = '''\
<?xml version="1.0"?>
<card:addressbook-multiget xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <d:getetag />
    <card:address-data />
  </d:prop>
  <d:href>%s</d:href>
</card:addressbook-multiget>
''' % '</d:href><d:href>'.join(urls)
        parameter = self._getRequestParameter('getAddressbookCards', user.Name, user.Password, addressbook.Path, data)
        response = request.executeRequest(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'mergeCardByToken()', user)
        count = database.mergeCard(addressbook.Id, self_parseCards(response))
        response.close()
        return count

    def _parseCards(self, response):
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._length, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag != '{DAV:}response':
                    continue
                url = tag = data = None
                for child in element.iter():
                    if child.tag == '{DAV:}href' and child.text:
                        url = child.text
                    elif child.tag == '{DAV:}getetag' and child.text:
                        tag = child.text
                    elif child.tag == '{urn:ietf:params:xml:ns:carddav}address-data' and child.text:
                        data = child.text
                if all((url, tag, data)):
                    yield url, tag, data

    def _getChangedCards(self, response):
        token = None
        deleted = []
        modified = []
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._length, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag == '{DAV:}response':
                    url = modified = None
                    for child in element.iter():
                        if child.tag == '{DAV:}href' and child.text:
                            url = child.text
                        elif child.tag == '{DAV:}status' and child.text:
                            status = True if child.text != self._status else False
                    if all((url, status is not None)):
                        modified.append(url) if status else deleted.append(url)
                elif element.tag == '{DAV:}sync-token':
                    token = element.text
        return token, deleted, modified

    def _getRequestParameter(self, method, user, password, url=None, data=None):
        parameter = uno.createUnoStruct('com.sun.star.rest.RequestParameter')
        parameter.Name = method
        if method == 'getUrl':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "0"}'
            parameter.NoRedirect = True
        elif method == 'getUser':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "0"}'
        elif method == 'hasAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'OPTIONS'
            parameter.Auth = (user, password)
        elif method == 'getAddressbooksUrl':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "0"}'
        elif method == 'getDefaultAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "1"}'

        elif method == 'getAllAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "1"}'



        elif method == 'getAddressbookUrl':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "1"}'
        elif method == 'getAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "1"}'
        elif method == 'getAddressbookCards':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'REPORT'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8", "Depth": "1"}'
        elif method == 'getModifiedCardByToken':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'REPORT'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Content-Type": "application/xml; charset=utf-8"}'
        return parameter

