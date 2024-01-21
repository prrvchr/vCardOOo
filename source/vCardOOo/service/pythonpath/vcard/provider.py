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

from .cardtool import getSqlException

from .card import Provider as ProviderBase

from .oauth2 import getRequest

from .configuration import g_identifier

import xml.etree.ElementTree as ET
import traceback


class Provider(ProviderBase):
    def __init__(self, ctx, database):
        ProviderBase.__init__(self, ctx)
        self._chunk = 256
        self._cardsync = '%s.CardSync' % g_identifier
        self._url = '/.well-known/carddav'
        self._header = 'addressbook'
        self._status = 'HTTP/1.1 404 Not Found'

    def supportAddressBook(self):
        return True

# Method called from DataSource.getConnection()
    def getUserUri(self, server, name):
        return server + '/' + name

    def initAddressbooks(self, source, database, user):
        parameter = self._getAllBookParameter(user)
        response = user.Request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(response, source, 'initAddressbooks()', 1006, parameter.Name, user.Name, parameter.Url)
        iterator = self._parseAllBook(response)
        self.initUserBooks(source, database, user, iterator)

    def initUserGroups(self, database, user, book):
        pass

    # Method called from User.__init__()
    # This method call Request without OAuth2 mode
    def getRequest(self, url, user):
        return getRequest(self._ctx)

    def insertUser(self, source, database, request, scheme, server, name, pwd):
        userid = self._getNewUserId(source, request, scheme, server, name, pwd)
        return database.insertUser(userid, scheme, server, '', name)

    # Private method
    def _getNewUserId(self, source, request, scheme, server, name, pwd):
        cls, mtd = 'Provider', '_getNewUserId()'
        url = scheme + server + self._url
        redirect, url = self._getDiscoveryUrl(source, request, url, name, pwd)
        if redirect:
            scheme, server = self._getUrlParts(url)
            redirect, url = self._getDiscoveryUrl(source, request, url, name, pwd)
        path = self._getUserUrl(source, request, url, name, pwd)
        if path is None:
            password = '*' * len(pwd)
            raise getSqlException(self._ctx, source, 1001, 1641, cls, mtd, name, password, server, url)
        url = scheme + server + path
        if not self._supportAddressbook(source, request, url, name, pwd):
            raise getSqlException(self._ctx, source, 1006, 1642, name, url)
        userid = self._getAddressbooksUrl(source, request, url, name, pwd)
        return userid

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location)
        scheme = url.Protocol
        server = url.Server
        return scheme, server

    def _getDiscoveryUrl(self, source, request, url, name, pwd):
        cls, mtd = 'Provider', '_getDiscoveryUrl()'
        parameter = self._getRequestParameter(request, 'getUrl', url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok or not response.IsRedirect:
            self.raiseForStatus(response, source, mtd, 1006, parameter.Name, name, parameter.Url)
        if not response.hasHeader('Location'):
            headers = response.Headers
            response.close()
            raise getSqlException(self._ctx, source, 1006, 1621, cls, mtd, parameter.Name, name, url, headers)
        location = response.getHeader('Location')
        response.close()
        redirect = location.endswith(self._url)
        return redirect, location

    def _getUserUrl(self, source, request, url, name, pwd):
        parameter = self._getUserUrlParameter(request, url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(response, source, '_getUserUrl()', 1006, parameter.Name, name, parameter.Url)
        url = self._parseUserUrl(response)
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
        response.close()
        return url

    def _supportAddressbook(self, source, request, url, name, pwd):
        cls, mtd = 'Provider', '_supportAddressbook()'
        parameter = self._getRequestParameter(request, 'hasAddressbook', url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(response, source, mtd, 1006, parameter.Name, name, parameter.Url)
        if not response.hasHeader('DAV'):
            headers = response.Headers
            response.close()
            raise getSqlException(self._ctx, source, 1006, 1651, cls, mtd, parameter.Name, name, url, headers)
        support = self._header in (header.strip() for header in response.getHeader('DAV').split(','))
        response.close()
        return support

    def _getAddressbooksUrl(self, source, request, url, name, pwd):
        cls, mtd = 'Provider', '_getAddressbooksUrl()'
        parameter = self._getAddressbooksUrlParameter(request, url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(response, source, mtd, 1006, parameter.Name, name, parameter.Url)
        url = self._parseAddressbookUrl(response)
        if url is None:
            msg = response.Text
            response.close()
            raise getSqlException(self._ctx, source, 1006, 1661, cls, mtd, parameter.Name, name, url, msg)
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

    def _parseAllBook(self, response):
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
        response.close()

    def _getAllBookParameter(self, user):
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
        return self._getRequestParameter(user.Request, 'getAllAddressbook', url, user.Name, user.Password, data)

    def _getUserUrlParameter(self, request, url, name, pwd):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:current-user-principal />
  </d:prop>
</d:propfind>
'''
        return self._getRequestParameter(request, 'getUser', url, name, pwd, data)

    def _getAddressbooksUrlParameter(self, request, url, name, pwd):
        data = '''\
<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
  <d:prop>
    <card:addressbook-home-set />
  </d:prop>
</d:propfind>
'''
        return self._getRequestParameter(request, 'getAddressbooksUrl', url, name, pwd, data)


# Method called from Replicator.run()
    def firstPullCard(self, database, user, addressbook, page, count):
        args = []
        parameter = self._getFisrtPullParameter(user, addressbook)
        response = user.Request.execute(parameter)
        if not response.Ok:
            cls, mtd = 'Provider', 'firstPullCard()'
            code = response.StatusCode
            msg = response.Text
            response.close()
            args += [cls, mtd, 201, parameter.Name, code, user.Name, parameter.Url, msg]
            return page, count, args
        page += 1
        iterator = self._parseCards(response)
        count += database.mergeCard(addressbook.Id, iterator)
        return page, count, args

    def pullCard(self, database, user, addressbook, page, count):
        if addressbook.Token is not None:
            page, count, args = self._pullCardByToken(database, user, addressbook, page, count)
        elif addressbook.Tag is not None:
            page, count, args = self._pullCardByTag(database, user, addressbook, page, count)
        return page, count, args

    def parseCard(self, database):
        url = 'vnd.sun.star.job:service=%s' % self._cardsync
        arguments = getPropertyValueSet({'Connection': database.Connection})
        executeDispatch(self._ctx, url, arguments)

    # Private method
    def _pullCardByToken(self, database, user, addressbook, page, count):
        parameter = self._getCardByTokenParameter(user, addressbook)
        response = user.Request.execute(parameter)
        if not response.Ok:
            cls, mtd = 'Provider', '_pullCardByToken()'
            code = response.StatusCode
            msg = response.Text
            response.close()
            args += [cls, mtd, 211, parameter.Name, code, user.Name, parameter.Url, msg]
            return page, count, args
        args = []
        token, deleted, modified = self._getChangedCards(response)
        if addressbook.Token != token:
            if deleted:
                count += database.deleteCard(deleted)
            if modified:
                count, args = self._mergeCardByToken(database, user, addressbook, modified, count)
            database.updateAddressbookToken(addressbook.Id, token)
        page += 1
        return page, count, args

    def _pullCardByTag(self, database, user, addressbook, page, count):
        # TODO: Need to be implemented method
        print("Provider._pullCardByTag() %s" % (addressbook.Name, ))
        return page, count, None

    def _mergeCardByToken(self, database, user, addressbook, urls, count):
        parameter = self._getMergeCardByTokenParameter(user, addressbook, urls)
        response = request.execute(parameter)
        if not response.Ok:
            cls, mtd = 'Provider', '_mergeCardByToken()'
            code = response.StatusCode
            msg = response.Text
            response.close()
            args = [cls, mtd, 221, parameter.Name, code, user.Name, parameter.Url, msg]
            return count, args
        iterator = self._parseCards(response)
        count += database.mergeCard(addressbook.Id, iterator)
        return count, []

    def _parseCards(self, response):
        deleted = False
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
                    yield url, tag, deleted, data
        response.close()

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
        response.close()
        return token, deleted, modified

    def _getFisrtPullParameter(self, user, addressbook):
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
        return self._getRequestParameter(user.Request, 'getAddressbookCards', url, user.Name, user.Password, data)

    def _getCardByTokenParameter(self, user, addressbook):
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
        return self._getRequestParameter(user.Request, 'getModifiedCardByToken', url, user.Name, user.Password, data)

    def _getMergeCardByTokenParameter(self, user, addressbook, urls):
        url = user.BaseUrl + addressbook.Uri
        href = '''\
  </d:href>
  <d:href>
'''
        data = '''\
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
''' % href.join(urls)
        return self._getRequestParameter(request, 'getAddressbookCards', url, user.Name, user.Password, data)


    # Private getter method for Request Parameter
    def _getRequestParameter(self, request, method, url, name, pwd, data=None):
        parameter = request.getRequestParameter(method)
        parameter.Url = url

        if method == 'getUrl':
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, pwd)
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')
            parameter.NoRedirect = True

        elif method == 'getUser':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, pwd)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')

        elif method == 'hasAddressbook':
            parameter.Url = url
            parameter.Method = 'OPTIONS'
            parameter.Auth = (name, pwd)

        elif method == 'getAddressbooksUrl':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, pwd)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '0')

        elif method == 'getAllAddressbook':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (name, pwd)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '1')

        elif method == 'getAddressbookCards':
            parameter.Url = url
            parameter.Method = 'REPORT'
            parameter.Auth = (name, pwd)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')
            parameter.setHeader('Depth', '1')

        elif method == 'getModifiedCardByToken':
            parameter.Url = url
            parameter.Method = 'REPORT'
            parameter.Auth = (name, pwd)
            parameter.Text = data
            parameter.setHeader('Content-Type', 'application/xml; charset=utf-8')

        return parameter

