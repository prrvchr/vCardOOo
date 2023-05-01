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

from .unotool import executeDispatch
from .unotool import getPropertyValueSet
from .unotool import getUrl

from .card import Provider as ProviderBase

from .configuration import g_identifier

import xml.etree.ElementTree as ET
import traceback


class Provider(ProviderBase):
    def __init__(self, ctx, database):
        self._ctx = ctx
        self._chunk = 256
        self._cardsync = '%s.CardSync' % g_identifier
        self._url = '/.well-known/carddav'
        self._headers = ('1', 'access-control', 'addressbook')
        self._status = 'HTTP/1.1 404 Not Found'

    # Method called from DataSource.getConnection()
    def getUserUri(self, server, name):
        return server + '/' + name

    # Method called from User._getNewUser()
    def insertUser(self, database, request, scheme, server, name, pwd):
        userid = self._getNewUserId(request, scheme, server, name, pwd)
        return database.insertUser(userid, scheme, server, '', name)

    def _getNewUserId(self, request, scheme, server, name, pwd):
        try:
            url = scheme + server + self._url
            redirect, url = self._getDiscoveryUrl(request, url, name, pwd)
            print("Provider.getNewUserId() 1 Redirect: %s - Url: %s" % (redirect, url))
            if redirect:
                scheme, server = self._getUrlParts(url)
                redirect, url = self._getDiscoveryUrl(request, url, name, pwd)
                print("Provider.getNewUserId() 2 Redirect: %s - Url: %s" % (redirect, url))
            path = self._getUserUrl(request, url, name, pwd)
            print("Provider.getNewUserId() 3 Path: %s" % (path, ))
            if path is None:
                #TODO: Raise SqlException with correct message!
                raise self.getSqlException(1004, 1108, 'getNewUserId', 'Server: %s Bad password: %s!' % (server, '*'*pwd))
            url = scheme + server + path
            if not self._supportAddressbook(request, url, name, pwd):
                #TODO: Raise SqlException with correct message!
                raise self.getSqlException(1004, 1108, 'getNewUserId', '%s has no support of CardDAV!' % server)
            print("Provider.getNewUserId() 4 %s" % path)
            userid = self._getAddressbooksUrl(request, url, name, pwd)
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
        scheme = url.Protocol
        server = url.Server
        return scheme, server

    def _getDiscoveryUrl(self, request, url, name, password):
        parameter = self._getRequestParameter(request, 'getUrl', url, name, password)
        response = request.execute(parameter)
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

    def _getUserUrl(self, request, url, name, password):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:current-user-principal />
  </d:prop>
</d:propfind>
'''
        parameter = self._getRequestParameter(request, 'getUser', url, name, password, data)
        response = request.execute(parameter)
        if not response.Ok:
            response.close()
            raise self.getSqlException(1006, 1107, 'getUserUrl()', name)
        url = self._parseUserUrl(response)
        response.close()
        return url

    def _parseUserUrl(self, response):
        url = None
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._chunk, False)
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

    def _supportAddressbook(self, request, url, name, password):
        parameter = self._getRequestParameter(request, 'hasAddressbook', url, name, password)
        response = request.execute(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'supportAddressbook()', name)
        headers = response.getHeader('DAV')
        response.close()
        for headers in self._headers:
            if headers not in headers:
                return False
        return True

    def _getAddressbooksUrl(self, request, url, name, pwd):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <card:addressbook-home-set />
  </d:prop>
</d:propfind>
'''
        parameter = self._getRequestParameter(request, 'getAddressbooksUrl', url, name, pwd, data)
        response = request.execute(parameter)
        if not response.Ok:
            response.close()
            raise self.getSqlException(1006, 1107, 'getAddressbooksUrl()', name)
        url = self._parseAddressbookUrl(response)
        response.close()
        return url

    def _parseAddressbookUrl(self, response):
        url = None
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._chunk, False)
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
        count, modified = self._updateAllAddressbook(database, user)
        if not count:
            #TODO: Raise SqlException with correct message!
            print("User.initAddressbooks() 1 %s" % (addressbooks, ))
            raise self.getSqlException(1004, 1108, 'initAddressbooks', '%s has no support of CardDAV!' % user.Server)
        if modified:
            database.initAddressbooks(user)

    def _updateAllAddressbook(self, database, user):
        url = user.BaseUrl + user.Uri
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
        parameter = self._getRequestParameter(user.Request, 'getAllAddressbook', url, user.Name, user.Password, data)
        response = user.Request.execute(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getAllAddressbook()', user.Name)
        count, modified = user.Addressbooks.initAddressbooks(database, user.Id, self._parseAllAddressbook(response))
        response.close()
        return count, modified

    def _parseAllAddressbook(self, response):
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._chunk, False)
        while iterator.hasMoreElements():
            # FIXME: As Decode is False we obtain a sequence of bytes
            parser.feed(iterator.nextElement().value)
            for event, element in parser.read_events():
                if element.tag != '{DAV:}response':
                    continue
                url = name = tag = token = None
                for child in element.iter():
                    if child.tag == '{DAV:}href' and child.text:
                        url = child.text
                    elif child.tag == '{DAV:}displayname' and child.text:
                        name = child.text
                    elif child.tag == '{http://calendarserver.org/ns/}getctag' and child.text:
                        tag = child.text
                    elif child.tag == '{DAV:}sync-token' and child.text:
                        token = child.text
                if all((url, name, tag, token)):
                    yield url, name, tag, token

    def firstPullCard(self, database, user, addressbook, page, count):
        url = user.BaseUrl + addressbook.Uri
        data = '''\
<?xml version="1.0"?>
<card:addressbook-query xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <d:getetag />
    <card:address-data />
  </d:prop>
</card:addressbook-query>
'''
        parameter = self._getRequestParameter(user.Request, 'getAddressbookCards', url, user.Name, user.Password, data)
        response = user.Request.execute(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getAddressbookCards()', user.Name)
        count += database.mergeCard(addressbook.Id, self._parseCards(response))
        response.close()
        return page + 1, count

    def pullCard(self, database, user, addressbook, page, count):
        if addressbook.Token is not None:
            page, count = self._pullCardByToken(database, user, addressbook, page, count)
        elif addressbook.Tag is not None:
            page, count = self._pullCardByTag(database, user, addressbook, page, count)
        return page, count

    def parseCard(self, database):
        url = 'vnd.sun.star.job:service=%s' % self._cardsync
        arguments = getPropertyValueSet({'Connection': database.Connection})
        executeDispatch(self._ctx, url, arguments)

    def _pullCardByToken(self, database, user, addressbook, page, count):
        token, deleted, modified = self._getCardByToken(user, addressbook)
        if addressbook.Token != token:
            if deleted:
                count += database.deleteCard(deleted)
            if modified:
                count += self._mergeCardByToken(database, user, addressbook)
            database.updateAddressbookToken(addressbook.Id, token)
        return page +1, count

    def _pullCardByTag(self, database, user, addressbook, page, count):
        print("Provider._pullCardByTag() %s" % (addressbook.Name, ))
        return page, count

    def _getCardByToken(self, user, addressbook):
        url = user.BaseUrl + addressbook.Uri
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
        parameter = self._getRequestParameter(user.Request, 'getModifiedCardByToken', url, user.Name, user.Password, data)
        response = user.Request.execute(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'getModifiedCardByToken()', user.Name)
        token, deleted, modified = self._getChangedCards(response)
        response.close()
        return token, deleted, modified

    def _mergeCardByToken(self, database, user, addressbook, urls):
        url = user.BaseUrl + addressbook.Uri
        body = '''\
<?xml version="1.0"?>
<card:addressbook-multiget xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <d:getetag />
    <card:address-data />
  </d:prop>
  <d:href>
    %s
  </d:href>
</card:addressbook-multiget>
'''
        href = '''\
  </d:href>
  <d:href>
'''
        data = body % href.join(urls)
        parameter = self._getRequestParameter(request, 'getAddressbookCards', url, user.Name, user.Password, data)
        response = request.execute(parameter)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self.getSqlException(1006, 1107, 'mergeCardByToken()', user.Name)
        count = database.mergeCard(addressbook.Id, self_parseCards(response))
        response.close()
        return count

    def _parseCards(self, response):
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._chunk, False)
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
                    yield url, tag, False, data

    def _getChangedCards(self, response):
        token = None
        deleted = []
        modified = []
        parser = ET.XMLPullParser(('end', ))
        iterator = response.iterContent(self._chunk, False)
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

    def _getRequestParameter(self, request, method, url, name, password, data=None):
        parameter = request.getRequestParameter(method)
        parameter.Url = url
        print("Provider._getRequestParameter() Name: %s - Password: %s" % (name, password))
        if method == 'getUrl':
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, password)
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')
            parameter.NoRedirect = True

        elif method == 'getUser':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, password)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')

        elif method == 'hasAddressbook':
            parameter.Url = url
            parameter.Method = 'OPTIONS'
            parameter.Auth = (name, password)

        elif method == 'getAddressbooksUrl':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, password)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')

        elif method == 'getAllAddressbook':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, password)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '1')

        elif method == 'getAddressbookCards':
            parameter.Url = url
            parameter.Method = 'REPORT'
            parameter.Auth = (name, password)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '1')

        elif method == 'getModifiedCardByToken':
            parameter.Url = url
            parameter.Method = 'REPORT'
            parameter.Auth = (name, password)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')

        return parameter

