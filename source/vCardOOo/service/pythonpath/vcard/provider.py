#!
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020-25 https://prrvchr.github.io                                  ║
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

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from .card import Provider as ProviderMain

from .unotool import executeDispatch
from .unotool import getUrl

from .helper import getSqlException

from .oauth20 import getRequest

from .configuration import g_identifier

import xml.etree.ElementTree as ET
import traceback


class Provider(ProviderMain):
    def __init__(self, ctx, src, database):
        ProviderMain.__init__(self, ctx, src)
        self._chunk = 256
        self._cardsync = '%s.CardSync' % g_identifier
        self._url = '/.well-known/carddav'
        self._header = 'addressbook'
        self._status = 'HTTP/1.1 404 Not Found'

    def supportAddressBook(self):
        return True

    def supportGroup(self):
        return False

# Method called from Provider.insertUser()
    def getNewUserId(self, request, scheme, server, name, pwd):
        url = self._getDiscoveryUrl(request, scheme, server, name, pwd)
        path = self._getUserUrl(request, url, name, pwd)
        if path is None:
            password = '*' * len(pwd)
            raise getSqlException(self._ctx, self._src, 1001, 1641, self._cls, 'getNewUserId', name, password, server, url)
        scheme, server = self._getUrlParts(url)
        url = scheme + server + path
        if not self._supportAddressbook(request, url, name, pwd):
            raise getSqlException(self._ctx, self._src, 1006, 1642, name, url)
        userid = self._getAddressbooksUrl(request, url, name, pwd)
        return userid

# Method called from DataSource.getConnection()
    def getUserUri(self, server, name):
        return server + '/' + name

# Method called from Provider.initAddressbooks()
    def getAddressbooks(self, database, user):
        parameter = self._getAllBookParameter(user)
        response = user.Request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(mtd, response, user.Name)
        return self._parseAllBook(response)

    def initUserGroups(self, database, user, book):
        pass

    # Method called from User.__init__()
    # This method call Request without OAuth2 mode
    def getRequest(self, url, user):
        return getRequest(self._ctx)

    # Private method
    def _getDiscoveryUrl(self, request, scheme, server, name, pwd):
        mtd = '_getDiscoveryUrl'
        attempt = retry = 3
        url = scheme + server + self._url
        while url.endswith(self._url) and retry > 0:
            url = self._discoverUrl(request, url, name, pwd)
            retry -= 1
        if url.endswith(self._url):
            raise getSqlException(self._ctx, self._src, 1006, 1622, self._cls, mtd, attempt, url)
        return url

    def _discoverUrl(self, request, url, name, pwd):
        mtd = '_discoverUrl'
        parameter = self._getRequestParameter(request, 'getUrl', url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(mtd, response, name)
        if not response.IsRedirect or not response.hasHeader('Location'):
            headers = response.Headers
            response.close()
            raise getSqlException(self._ctx, self._src, 1006, 1621, self._cls, mtd, parameter.Name, name, url, headers)
        location = response.getHeader('Location')
        response.close()
        return location

    def _getUserUrl(self, request, url, name, pwd):
        parameter = self._getUserUrlParameter(request, url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus('_getUserUrl', response, name)
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

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location)
        scheme = url.Protocol
        server = url.Server
        return scheme, server

    def _supportAddressbook(self, request, url, name, pwd):
        mtd = '_supportAddressbook'
        parameter = self._getRequestParameter(request, 'hasAddressbook', url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(mtd, response, name)
        if not response.hasHeader('DAV'):
            headers = response.Headers
            response.close()
            raise getSqlException(self._ctx, self._src, 1006, 1651, self._cls, mtd, parameter.Name, name, url, headers)
        support = self._header in (header.strip() for header in response.getHeader('DAV').split(','))
        response.close()
        return support

    def _getAddressbooksUrl(self, request, url, name, pwd):
        mtd = '_getAddressbooksUrl'
        parameter = self._getAddressbooksUrlParameter(request, url, name, pwd)
        response = request.execute(parameter)
        if not response.Ok:
            self.raiseForStatus(mtd, response, name)
        url = self._parseAddressbookUrl(response)
        if url is None:
            msg = response.Text
            response.close()
            raise getSqlException(self._ctx, self._src, 1006, 1661, self._cls, mtd, parameter.Name, name, url, msg)
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
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:carddav" xmlns:CS="http://calendarserver.org/ns/">
  <D:prop>
    <D:displayname />
    <CS:getctag />
    <D:sync-token />
    <D:resourcetype>
        <C:addressbook />
    </D:resourcetype>
  </D:prop>
</D:propfind>
'''
        return self._getRequestParameter(user.Request, 'getAllAddressbook', url, user.Name, user.Password, data)

    def _getUserUrlParameter(self, request, url, name, pwd):
        data = '''\
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:">
  <D:prop>
    <D:current-user-principal />
  </D:prop>
</D:propfind>
'''
        return self._getRequestParameter(request, 'getUser', url, name, pwd, data)

    def _getAddressbooksUrlParameter(self, request, url, name, pwd):
        data = '''\
<?xml version="1.0" encoding="utf-8" ?>
<D:propfind xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:carddav">
  <D:prop>
    <C:addressbook-home-set />
  </D:prop>
</D:propfind>
'''
        return self._getRequestParameter(request, 'getAddressbooksUrl', url, name, pwd, data)


# Method called from Replicator.run()
    def firstPullCard(self, database, user, book, page, count):
        parameter = self._getFisrtPullParameter(user, book)
        response = user.Request.execute(parameter)
        if not response.Ok:
            args = self.getLoggerArgs(response, 'firstPullCard()', parameter, user.Name)
            return page, count, args
        page += 1
        iterator = self._parseCards(response)
        count += database.mergeCard(book.Id, iterator)
        return page, count, []

    def pullCard(self, database, user, book, page, count):
        if book.Token is not None:
            page, count, args = self._pullCardByToken(database, user, book, page, count)
        elif book.Tag is not None:
            page, count, args = self._pullCardByTag(database, user, book, page, count)
        return page, count, args

    def parseCard(self, database):
        url = 'vnd.sun.star.job:service=%s' % self._cardsync
        args = {'Connection': database.Connection}
        executeDispatch(self._ctx, url, **args)

    # Private method
    def _pullCardByToken(self, database, user, book, page, count):
        parameter = self._getCardByTokenParameter(user, book)
        response = user.Request.execute(parameter)
        if not response.Ok:
            args = self.getLoggerArgs(response, '_pullCardByToken()', parameter, user.Name)
            return page, count, args
        args = []
        token, deleted, modified = self._getChangedCards(response)
        if book.Token != token:
            if deleted:
                count += database.deleteCard(deleted)
            if modified:
                count, args = self._mergeCardByToken(database, user, book, modified, count)
            database.updateAddressbookToken(book.Id, token)
        page += 1
        return page, count, args

    def _pullCardByTag(self, database, user, book, page, count):
        # TODO: Need to be implemented method
        print("Provider._pullCardByTag() %s" % (book.Name, ))
        return page, count, None

    def _mergeCardByToken(self, database, user, book, urls, count):
        parameter = self._getMergeCardByTokenParameter(user, book, urls)
        response = user.Request.execute(parameter)
        if not response.Ok:
            args = self.getLoggerArgs(response, '_mergeCardByToken()', parameter, user.Name)
            return count, args
        iterator = self._parseCards(response)
        count += database.mergeCard(book.Id, iterator)
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
                    url = status = None
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

    def _getFisrtPullParameter(self, user, book):
        url = user.BaseUrl + book.Uri
        data = '''\
<?xml version="1.0" encoding="utf-8" ?>
<C:addressbook-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:carddav">
  <D:prop>
    <D:getetag />
    <C:address-data />
  </D:prop>
</C:addressbook-query>
'''
        return self._getRequestParameter(user.Request, 'getAddressbookCards', url, user.Name, user.Password, data)

    def _getCardByTokenParameter(self, user, book):
        url = user.BaseUrl + book.Uri
        data = '''\
<?xml version="1.0" encoding="utf-8" ?>
<D:sync-collection xmlns:D="DAV:">
  <D:sync-token>%s</D:sync-token>
  <D:sync-level>1</D:sync-level>
  <D:prop>
    <D:getetag />
  </D:prop>
</D:sync-collection>
''' % book.Token
        return self._getRequestParameter(user.Request, 'getModifiedCardByToken', url, user.Name, user.Password, data)

    def _getMergeCardByTokenParameter(self, user, book, urls):
        url = user.BaseUrl + book.Uri
        href = '''</D:href>
  <D:href>'''
        data = '''\
<?xml version="1.0" encoding="utf-8" ?>
<C:addressbook-multiget xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:carddav">
  <D:prop>
    <D:getetag />
    <C:address-data />
  </D:prop>
  <D:href>%s</D:href>
</C:addressbook-multiget>
''' % href.join(urls)
        return self._getRequestParameter(user.Request, 'getAddressbookCards', url, user.Name, user.Password, data)


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

