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

from com.sun.star.ucb.ConnectionMode import OFFLINE
from com.sun.star.ucb.ConnectionMode import ONLINE
from com.sun.star.auth.RestRequestTokenType import TOKEN_NONE
from com.sun.star.auth.RestRequestTokenType import TOKEN_URL
from com.sun.star.auth.RestRequestTokenType import TOKEN_REDIRECT
from com.sun.star.auth.RestRequestTokenType import TOKEN_QUERY
from com.sun.star.auth.RestRequestTokenType import TOKEN_JSON
from com.sun.star.auth.RestRequestTokenType import TOKEN_SYNC

from com.sun.star.sdbc import XRestProvider

from .dataparser import DataParser

from .unotool import getConnectionMode
from .unotool import getUrl

from .dbtool import getSqlException

from .configuration import g_host
from .configuration import g_url
from .configuration import g_page
from .configuration import g_member
from .logger import logMessage
from .logger import getMessage
g_message = 'datasource'

import json


class Provider(unohelper.Base,
               XRestProvider):
    def __init__(self, ctx, scheme, server):
        self._ctx = ctx
        self._scheme = scheme
        self._server = server
        self._url = '/.well-known/carddav'
        self._headers = ('1', 'access-control', 'addressbook')
        self._Error = ''
        self.SessionMode = OFFLINE

    @property
    def Host(self):
        return self._server
    @property
    def BaseUrl(self):
        return self._scheme + self._server

    def isOnLine(self):
        return getConnectionMode(self._ctx, self.Host) != OFFLINE
    def isOffLine(self):
        offline = getConnectionMode(self._ctx, self.Host) != ONLINE
        print("Provider.isOffLine() %s" % offline)
        return offline

    def getWellKnownUrl(self):
        return self._scheme + self._server + self._url

    def getUrlParts(self, location):
        url = getUrl(self._ctx, location)
        self._scheme = url.Protocol
        self._server = url.Server
        return self._scheme, self._server

    def transcode(self, name, value):
        if name == 'People':
            value = self._getResource('people', value)
        elif name == 'Group':
            value = self._getResource('contactGroups', value)
        return value
    def transform(self, name, value):
        #if name == 'Resource' and value.startswith('people'):
        #    value = value.split('/').pop()
        return value

    def getDiscoveryUrl(self, request, user, password, url):
        parameter = self._getRequestParameter('getUrl', user, password, url)
        response = request.getResponse(parameter, None)
        if not response.Ok or not response.IsRedirect:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, '%s Response not Ok' % url)
        location = response.getHeader('Location')
        response.close()
        if not location:
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, '%s url is None' % url)
        redirect = location.endswith(self._url)
        return redirect, location

    def getUserUrl(self, request, user, password, url):
        data = '''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:current-user-principal/>
  </d:prop>
</d:propfind>'''
        parameter = self._getRequestParameter('getUser', user, password, url, data)
        parser = DataParser(parameter.Name)
        response = request.getResponse(parameter, parser)
        if not response.Ok:
            response.close()
            raise self._getSqlException(1006, 1107, user)
        url = response.Data
        response.close()
        return url

    def supportAddressbook(self, request, user, password, url):
        parameter = self._getRequestParameter('hasAddressbook', user, password, url)
        response = request.getResponse(parameter, None)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, user)
        headers = response.getHeader('DAV')
        response.close()
        for headers in self._headers:
            if headers not in headers:
                return False
        return True

    def getAddressbooksUrl(self, request, user, password, url):
        data = '''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <card:addressbook-home-set xmlns:card="urn:ietf:params:xml:ns:carddav"/>
  </d:prop>
</d:propfind>'''
        parameter = self._getRequestParameter('getAddressbooksUrl', user, password, url, data)
        parser = DataParser(parameter.Name)
        response = request.getResponse(parameter, parser)
        if not response.Ok:
            response.close()
            raise self._getSqlException(1006, 1107, user)
        url = response.Data
        response.close()
        return url

    def getDefaultAddressbook(self, request, user, password, url):
        data = '''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:displayname/>
    <d:resourcetype>
        <card:addressbook xmlns:card="urn:ietf:params:xml:ns:carddav"/>
    </d:resourcetype>
  </d:prop>
</d:propfind>'''
        parameter = self._getRequestParameter('getDefaultAddressbook', user, password, url, data)
        parser = DataParser(parameter.Name)
        response = request.getResponse(parameter, parser)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, user)
        name = response.Data
        response.close()
        return name

    def getAddressbookUrl(self, request, addressbook, user, password, url):
        data = '''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:displayname/>
    <d:resourcetype>
        <card:addressbook xmlns:card="urn:ietf:params:xml:ns:carddav"/>
    </d:resourcetype>
  </d:prop>
</d:propfind>'''
        parameter = self._getRequestParameter('getAddressbookUrl', user, password, url, data)
        parser = DataParser(parameter.Name, addressbook)
        response = request.getResponse(parameter, parser)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, user)
        url, name = response.Data
        response.close()
        return url, name

    def getAddressbook(self, request, addressbook, user, password, url):
        data = '''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:displayname/>
    <d:resourcetype>
        <card:addressbook xmlns:card="urn:ietf:params:xml:ns:carddav"/>
    </d:resourcetype>
  </d:prop>
</d:propfind>'''
        parameter = self._getRequestParameter('getAddressbook', user, password, url, data)
        parser = DataParser(parameter.Name, addressbook)
        response = request.getResponse(parameter, parser)
        if not response.Ok:
            response.close()
            #TODO: Raise SqlException with correct message!
            raise self._getSqlException(1006, 1107, user)
        isopen = response.Data == url
        response.close()
        return isopen


    def getUserId(self, user):
        return user.getValue('resourceName').split('/').pop()
        #return user.getValue('resourceName')
    def getItemId(self, item):
        return item.getDefaultValue('resourceName', '').split('/').pop()

    def _getResource(self, resource, keys):
        groups = []
        for k in keys:
            groups.append('%s/%s' % (resource, k))
        return tuple(groups)

    def _getRequestParameter(self, method, user, password, url=None, data=None):
        parameter = uno.createUnoStruct('com.sun.star.auth.RestRequestParameter')
        parameter.Name = method
        if method == 'getUrl':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Header = '{"Depth": "0"}'
            parameter.NoRedirect = True
        elif method == 'getUser':
            parameter.Url = url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Depth": "0"}'
        elif method == 'hasAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'OPTIONS'
            parameter.Auth = (user, password)
        elif method == 'getAddressbooksUrl':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Depth": "0"}'
        elif method == 'getDefaultAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Depth": "1"}'
        elif method == 'getAddressbookUrl':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Depth": "1"}'
        elif method == 'getAddressbook':
            parameter.Url = self.BaseUrl + url
            parameter.Method = 'PROPFIND'
            parameter.Auth = (user, password)
            parameter.Data = data
            parameter.Header = '{"Depth": "1"}'
        elif method == 'People':
            parameter.Method = 'GET'
            parameter.Url += '/people/me/connections'
            fields = '"personFields": "%s"' % ','.join(data.Fields)
            sources = '"sources": "READ_SOURCE_TYPE_CONTACT"'
            page = '"pageSize": %s' % g_page
            sync = data.PeopleSync
            if sync:
                token = '"syncToken": "%s"' % sync
            else:
                token = '"requestSyncToken": true'
            parameter.Query = '{%s, %s, %s, %s}' % (fields, sources, page, token)
            token = uno.createUnoStruct('com.sun.star.auth.RestRequestToken')
            token.Type = TOKEN_QUERY | TOKEN_SYNC
            token.Field = 'nextPageToken'
            token.Value = 'pageToken'
            token.SyncField = 'nextSyncToken'
            enumerator = uno.createUnoStruct('com.sun.star.auth.RestRequestEnumerator')
            enumerator.Field = 'connections'
            enumerator.Token = token
            parameter.Enumerator = enumerator
        elif method == 'Group':
            parameter.Method = 'GET'
            parameter.Url += '/contactGroups'
            page = '"pageSize": %s' % g_page
            query = [page]
            sync = data.GroupSync
            if sync:
                query.append('"syncToken": "%s"' % sync)
            parameter.Query = '{%s}' % ','.join(query)
            token = uno.createUnoStruct('com.sun.star.auth.RestRequestToken')
            token.Type = TOKEN_QUERY | TOKEN_SYNC
            token.Field = 'nextPageToken'
            token.Value = 'pageToken'
            token.SyncField = 'nextSyncToken'
            enumerator = uno.createUnoStruct('com.sun.star.auth.RestRequestEnumerator')
            enumerator.Field = 'contactGroups'
            enumerator.Token = token
            parameter.Enumerator = enumerator
        elif method == 'Connection':
            parameter.Method = 'GET'
            parameter.Url += '/contactGroups:batchGet'
            resources = '","'.join(data.getKeys())
            parameter.Query = '{"resourceNames": ["%s"], "maxMembers": %s}' % (resources, g_member)
        return parameter

    def _checkAddressbookHeader(self, headers):
        for headers in self._headers:
            if headers not in headers:
                return False
        return True

    def _getSqlException(self, state, code, format):
        state = getMessage(self._ctx, g_message, state)
        msg = getMessage(self._ctx, g_message, code, format)
        error = getSqlException(state, code, msg, self)
        return error
