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
import unohelper

from com.sun.star.lang import XServiceInfo

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from com.sun.star.sdbc import SQLException
from com.sun.star.sdbc import XDriver

from com.sun.star.sdbcx import XCreateCatalog
from com.sun.star.sdbcx import XDataDefinitionSupplier
from com.sun.star.sdbcx import XDropCatalog

from .datasource import DataSource

from .helper import getLogException

from .dbtool import getConnectionUrl
from .dbtool import getDriverPropertyInfos

from .unotool import getUrl

from .logger import getLogger

from .dbconfig import g_folder

from .configuration import g_defaultlog
from .configuration import g_identifier
from .configuration import g_protocol
from .configuration import g_scheme
from .configuration import g_host

import traceback


class Driver(unohelper.Base,
             XCreateCatalog,
             XDataDefinitionSupplier,
             XDriver,
             XDropCatalog,
             XServiceInfo):
    def __init__(self, ctx, logger, implementation, services):
        self._ctx = ctx
        self._cls = 'Driver'
        self._implementation = implementation
        self._services = services
        self._supportedProtocol = g_protocol
        self._logger = logger
        self._datasource = None

    @property
    def DataSource(self):
        if self._datasource is None:
            url = getConnectionUrl(self._ctx, g_folder + '/' + g_host)
            self._datasource = DataSource(self._ctx, self, self._logger, url)
        return self._datasource

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
        return service in self._services

    def getImplementationName(self):
        return self._implementation

    def getSupportedServiceNames(self):
        return self._services

# Private getter methods
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

