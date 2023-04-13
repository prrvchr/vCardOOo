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

from com.sun.star.lang import XServiceInfo

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from com.sun.star.sdbc import SQLException
from com.sun.star.sdbc import XDriver

from com.sun.star.sdbcx import XCreateCatalog
from com.sun.star.sdbcx import XDataDefinitionSupplier
from com.sun.star.sdbcx import XDropCatalog

from vcard import DataSource

from vcard import getDriverPropertyInfos
from vcard import getResourceLocation
from vcard import getSqlException
from vcard import getUrl

from vcard import getLogger
g_basename = 'Driver'

from vcard import g_identifier
from vcard import g_scheme
from vcard import g_host
from vcard import g_defaultlog

import traceback

# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationName = '%s.Driver' % g_identifier


class Driver(unohelper.Base,
             XCreateCatalog,
             XDataDefinitionSupplier,
             XDriver,
             XDropCatalog,
             XServiceInfo):
    def __init__(self, ctx):
        self._ctx = ctx
        self._supportedProtocol = 'sdbc:address:vcard'
        self._logger = getLogger(ctx, g_defaultlog, g_basename)
        self._logger.logprb(INFO, 'Driver', '__init__()', 101)

    _datasource = None

    @property
    def DataSource(self):
        if Driver._datasource is None:
            Driver._datasource = DataSource(self._ctx)
        return Driver._datasource

# XCreateCatalog
    def createCatalog(self, info):
        pass

# XDataDefinitionSupplier
    def getDataDefinitionByConnection(self, connection):
        return connection
    def getDataDefinitionByURL(self, url, infos):
        connection = self.connect(url, infos)
        return self.getDataDefinitionByConnection(connection)

# XDriver
    def connect(self, url, infos):
        try:
            self._logger.logprb(INFO, 'Driver', 'connect()', 111, url)
            protocols = url.strip().split(':')
            if len(protocols) < 4 or not all(protocols):
                raise self._getSqlException(112, 1101, 'connect()', url)
            location = ':'.join(protocols[3:]).strip('/')
            scheme, server = self._getUrlParts(location)
            if not server:
                raise self._getSqlException(112, 1101, 'connect()', url)
            user, pwd = self._getUserCredential(infos)
            if not user or not pwd:
                raise self._getSqlException(113, 1102, 'connect()', user)
            connection = self.DataSource.getConnection(scheme, server, user, pwd)
            version = connection.getMetaData().getDriverVersion()
            name = connection.getMetaData().getUserName()
            self._logger.logprb(INFO, 'Driver', 'connect()', 114, version, name)
            return connection
        except SQLException as e:
            raise e
        except Exception as e:
            self._logger.logprb(SEVERE, 'Driver', 'connect()', 115, e, traceback.format_exc())

    def acceptsURL(self, url):
        accept = url.startswith(self._supportedProtocol)
        return accept

    def getPropertyInfo(self, url, infos):
        properties = ()
        if self.acceptsURL(url):
            properties = getDriverPropertyInfos()
        return properties

    def getMajorVersion(self):
        return 1
    def getMinorVersion(self):
        return 0

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location, g_scheme)
        if url is None:
            raise self._getSqlException(112, 1101, '_getUrlParts()', location)
        scheme = url.Protocol
        server = url.Server
        if not location.startswith(scheme):
            scheme = g_scheme
        return scheme, server

    def _getUserCredential(self, infos):
        user = ''
        pwd = ''
        for info in infos:
            if info.Name == 'user':
                user = info.Value.strip()
            elif info.Name == 'password':
                pwd = info.Value.strip()
            if user and pwd:
                break
        return user, pwd

    def _getSqlException(self, state, code, method, *args):
        state = self._logger.resolveString(state)
        msg = self._logger.resolveString(code, *args)
        self._logger.logp(SEVERE, g_basename, method, msg)
        error = getSqlException(state, code, msg, self)
        return error

# XDropCatalog
    def dropCatalog(self, name, info):
        pass

# XServiceInfo
    def supportsService(self, service):
        return g_ImplementationHelper.supportsService(g_ImplementationName, service)
    def getImplementationName(self):
        return g_ImplementationName
    def getSupportedServiceNames(self):
        return g_ImplementationHelper.getSupportedServiceNames(g_ImplementationName)


g_ImplementationHelper.addImplementation(Driver,
                                         g_ImplementationName,
                                        (g_ImplementationName,
                                        'com.sun.star.sdbc.Driver',
                                        'com.sun.star.sdbcx.Driver'))
