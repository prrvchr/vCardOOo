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
from com.sun.star.awt import XContainerWindowEventHandler

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from vcard import LogManager

from vcard import createService
from vcard import getDesktop
from vcard import getDialog
from vcard import getFileSequence
from vcard import getSimpleFile
from vcard import getStringResource
from vcard import getResourceLocation

from vcard import clearLogger
from vcard import getLoggerSetting
from vcard import getLoggerUrl
from vcard import getMessage
from vcard import logMessage
from vcard import setLoggerSetting
g_logger = 'Logger'

from vcard import g_extension
from vcard import g_identifier
from vcard import g_host
from vcard import g_folder

import os
import sys
import traceback

# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationName = '%s.OptionsDialog' % g_identifier


class OptionsDialog(unohelper.Base,
                    XServiceInfo,
                    XContainerWindowEventHandler):
    def __init__(self, ctx):
        self._ctx = ctx
        self._logger = None

    # XContainerWindowEventHandler
    def callHandlerMethod(self, dialog, event, method):
        handled = False
        if method == 'external_event':
            if event == 'initialize':
                print("OptionsDialog.callHandlerMethod() ******** initialize")
                self._loadSetting(dialog)
                handled = True
            elif event == 'ok':
                self._saveSetting()
                handled = True
            elif event == 'back':
                self._reloadSetting()
                handled = True
        elif method == 'ViewData':
            self._viewData(dialog)
            handled = True
        return handled
    def getSupportedMethodNames(self):
        return ('external_event',
                'ViewData')

    def _loadSetting(self, dialog):
        version  = ' '.join(sys.version.split())
        path = os.pathsep.join(sys.path)
        infos = {111: version, 112: path}
        self._logger = LogManager(self._ctx, dialog.Peer, g_extension, infos)

    def _saveSetting(self):
        self._logger.saveLoggerSetting()

    def _reloadSetting(self):
        self._logger.setLoggerSetting()

    def _viewData(self, dialog):
        folder = g_folder + '/' + g_host
        location = getResourceLocation(self._ctx, g_identifier, folder)
        url = location + '.odb'
        if getSimpleFile(self._ctx).exists(url):
            desktop = getDesktop(self._ctx)
            desktop.loadComponentFromURL(url, '_default', 0, ())

    # XServiceInfo
    def supportsService(self, service):
        return g_ImplementationHelper.supportsService(g_ImplementationName, service)
    def getImplementationName(self):
        return g_ImplementationName
    def getSupportedServiceNames(self):
        return g_ImplementationHelper.getSupportedServiceNames(g_ImplementationName)


g_ImplementationHelper.addImplementation(OptionsDialog,                             # UNO object class
                                         g_ImplementationName,                      # Implementation name
                                        (g_ImplementationName,))                    # List of implemented services
