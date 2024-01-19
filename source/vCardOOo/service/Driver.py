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

from vcard import DataBase

from vcard import DataSource

from vcard import checkVersion
from vcard import getConnectionUrl
from vcard import getDriverPropertyInfos
from vcard import getExtensionVersion
from vcard import getLogger
from vcard import getOAuth2Version
from vcard import getLogException
from vcard import getUrl

from vcard import g_oauth2ext
from vcard import g_oauth2ver

from vcard import g_jdbcext
from vcard import g_jdbcid
from vcard import g_jdbcver

from vcard import g_extension
from vcard import g_identifier
from vcard import g_protocol
from vcard import g_scheme
from vcard import g_host
from vcard import g_folder
from vcard import g_defaultlog
from vcard import g_version

import traceback

# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationName = f'{g_identifier}.Driver'


class Driver(unohelper.Base,
             XCreateCatalog,
             XDataDefinitionSupplier,
             XDriver,
             XDropCatalog,
             XServiceInfo):
    def __init__(self, ctx):
        self._ctx = ctx
        self._supportedProtocol = g_protocol
        self._logger = getLogger(ctx, g_defaultlog)
        self._logger.logprb(INFO, 'Driver', '__init__()', 1101)

    __datasource = None

    @property
    def DataSource(self):
        if Driver.__datasource is None:
            Driver.__datasource = self._getDataSource()
        return Driver.__datasource

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
        cls, mtd = 'Driver', 'connect()'
        try:
            self._logger.logprb(INFO, cls, mtd, 1111, url)
            protocols = url.strip().split(':')
            if len(protocols) < 4 or not all(protocols):
                raise getLogException(self._logger, self, 1000, 1112, cls, mtd, url)
            location = ':'.join(protocols[3:]).strip('/')
            scheme, server = self._getUrlParts(location)
            if not server:
                raise getLogException(self._logger, self, 1000, 1112, cls, mtd, url)
            username, password = self._getUserCredential(infos)
            if not username or not password:
                raise getLogException(self._logger, self, 1001, 1113, cls, mtd)
            connection = self.DataSource.getConnection(self, scheme, server, username, password)
            version = self.DataSource.DataBase.Version
            name = connection.getMetaData().getUserName()
            self._logger.logprb(INFO, cls, mtd, 1114, version, name)
            return connection
        except SQLException as e:
            raise e
        except Exception as e:
            self._logger.logprb(SEVERE, cls, mtd, 1115, e, traceback.format_exc())

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

# Private getter methods
    def _getDataSource(self):
        cls, mtd = 'Driver', '_getDataSource()'
        oauth2 = getOAuth2Version(self._ctx)
        driver = getExtensionVersion(self._ctx, g_jdbcid)
        if oauth2 is None:
            raise getLogException(self._logger, self, 1000, 1121, cls, mtd, g_oauth2ext, g_extension)
        elif not checkVersion(oauth2, g_oauth2ver):
            raise getLogException(self._logger, self, 1000, 1122, cls, mtd, g_oauth2ext, g_oauth2ver)
        elif driver is None:
            raise getLogException(self._logger, self, 1000, 1121, cls, mtd, g_jdbcext, g_extension)
        elif not checkVersion(driver, g_jdbcver):
            raise getLogException(self._logger, self, 1000, 1122, cls, mtd, g_jdbcext, g_jdbcver)
        else:
            path = g_folder + '/' + g_host
            url = getConnectionUrl(self._ctx, path)
            try:
                database = DataBase(self._ctx, url)
            except SQLException as e:
                raise getLogException(self._logger, self, 1005, 1123, cls, mtd, url, e.Message)
            else:
                if not database.isUptoDate():
                    raise getLogException(self._logger, self, 1005, 1124, cls, mtd, database.Version, g_version)
                else:
                    return DataSource(self._ctx, database)
        return None

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location, g_scheme)
        if url is None:
            cls, mtd = 'Driver', '_getUrlParts()'
            raise getLogException(self._logger, self, 1000, 1131, cls, mtd, location)
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


g_ImplementationHelper.addImplementation(Driver,
                                         g_ImplementationName,
                                        (g_ImplementationName,
                                        'com.sun.star.sdbc.Driver',
                                        'com.sun.star.sdbcx.Driver'))
