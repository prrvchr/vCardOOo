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

from vcard import getDataSourceUrl
from vcard import getDriverPropertyInfos
from vcard import getLogger
from vcard import getLogException
from vcard import getUrl

from vcard import g_defaultlog
from vcard import g_protocol
from vcard import g_version

from vcard import g_identifier
from vcard import g_scheme


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
        self._cls = 'Driver'
        mtd = '__init__'
        self._ctx = ctx
        self._supportedProtocol = g_protocol
        self._logger = getLogger(ctx, g_defaultlog)
        self._logger.logprb(INFO, self._cls, mtd, 1101)

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
        return self.connect(url, infos)

# XDriver
    def connect(self, url, infos):
        try:
            mtd = 'connect'
            self._logger.logprb(INFO, self._cls, mtd, 1111, url)
            protocols = url.strip().split(':')
            if len(protocols) < 4 or not all(protocols):
                raise getLogException(self._logger, self, 1000, 1112, self._cls, mtd, url)
            location = ':'.join(protocols[3:]).strip('/')
            scheme, server = self._getUrlParts(location)
            if not server:
                raise getLogException(self._logger, self, 1000, 1112, self._cls, mtd, url)
            username, password = self._getUserCredential(infos)
            if not username or not password:
                raise getLogException(self._logger, self, 1001, 1113, self._cls, mtd)
            connection = self.DataSource.getConnection(self, self._logger, server, scheme, server, username, password)
            version = self.DataSource.DataBase.Version
            name = connection.getMetaData().getUserName()
            self._logger.logprb(INFO, self._cls, mtd, 1115, version, name)
            return connection
        except SQLException as e:
            raise e
        except Exception as e:
            raise getLogException(self._logger, self, 1005, 1116, self._cls, mtd, str(e), traceback.format_exc())

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
        mtd = '_getDataSource'
        url = getDataSourceUrl(self._ctx, self._logger, self, 1003, 1121, self._cls, mtd)
        try:
            datasource = DataSource(self._ctx, self._logger, url)
        except SQLException as e:
            raise getLogException(self._logger, self, 1005, 1123, self._cls, mtd, url, e.Message)
        except Exception as e:
            raise getLogException(self._logger, self, 1005, 1123, self._cls, mtd, url, str(e))
        if not datasource.isUptoDate():
            raise getLogException(self._logger, self, 1005, 1124, self._cls, mtd, datasource.getDataBaseVersion(), g_version)
        return datasource

    def _getUrlParts(self, location):
        url = getUrl(self._ctx, location, g_scheme)
        if url is None:
            raise getLogException(self._logger, self, 1000, 1131, self._cls, '_getUrlParts', location)
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
