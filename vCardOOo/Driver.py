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

from vcard import logMessage
from vcard import getMessage
g_message = 'Driver'

from vcard import g_identifier
from vcard import g_host

from vcard import g_class
from vcard import g_folder
from vcard import g_jar

import validators
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
        msg = getMessage(ctx, g_message, 101)
        logMessage(ctx, INFO, msg, 'Driver', '__init__()')

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
            msg = getMessage(self._ctx, g_message, 111, url)
            logMessage(self._ctx, INFO, msg, 'Driver', 'connect()')
            protocols = url.strip().split(':')
            if len(protocols) != 4 or not all(protocols):
                state = getMessage(self._ctx, g_message, 112)
                msg = getMessage(self._ctx, g_message, 1101, url)
                raise getSqlException(state, 1101, msg, self)
            server = protocols[3]
            user, password = self._getUserCredential(infos)
            print("Driver.connect() 1 %s - %s - %s" % (server, user, password))
            #if not validators.email(user):
            #    state = getMessage(self._ctx, g_message, 113)
            #    msg = getMessage(self._ctx, g_message, 1102, user)
            #    msg += getMessage(self._ctx, g_message, 1103)
            #    raise getSqlException(state, 1104, msg, self)
            msg = getMessage(self._ctx, g_message, 114, g_host)
            logMessage(self._ctx, INFO, msg, 'Driver', 'connect()')
            self.DataSource.setUser(server, user, password)
            msg = getMessage(self._ctx, g_message, 118, user)
            logMessage(self._ctx, INFO, msg, 'Driver', 'connect()')
            connection = self.DataSource.getConnection(user, password)
            msg = getMessage(self._ctx, g_message, 119, user)
            logMessage(self._ctx, INFO, msg, 'Driver', 'connect()')
            version = connection.getMetaData().getDriverVersion()
            msg = getMessage(self._ctx, g_message, 120, (version, user))
            logMessage(self._ctx, INFO, msg, 'Driver', 'connect()')
            print("Driver.connect() 2 %s - %s - %s - %s" % (server, user, password, version))
            return connection
        except SQLException as e:
            raise e
        except Exception as e:
            msg = getMessage(self._ctx, g_message, 121, (e, traceback.print_exc()))
            logMessage(self._ctx, SEVERE, msg, 'Driver', 'connect()')
            print(msg)

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

    def _getUserCredential(self, infos):
        user = ''
        password = ''
        for info in infos:
            if info.Name == 'user':
                user = info.Value.strip()
            elif info.Name == 'password':
                password = info.Value.strip()
            if user and password:
                break
        return user, password

    def _getDataSourceClassPath(self):
        path = '%s/%s' % (g_folder, g_jar)
        return getResourceLocation(self.ctx, g_identifier, path)

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
