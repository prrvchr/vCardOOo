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

from com.sun.star.logging.LogLevel import SEVERE

from .optionview import OptionView
from .optionhandler import WindowHandler

from ..options import OptionsManager

from ..unotool import createService
from ..unotool import executeFrameDispatch
from ..unotool import getDesktop
from ..unotool import getPropertyValueSet

from ..configuration import g_extension

import traceback


class OptionManager():
    def __init__(self, ctx, window, logger, offset):
        self._ctx = ctx
        self._module = 'CardDAVDiscoveryUrl'
        self._sub = 'Main'
        self._line = 26
        self._optionsmanager = OptionsManager(ctx, window, logger, offset)
        self._view = OptionView(ctx, window, WindowHandler(self))
        self._logger = logger

    def saveSetting(self):
        self._optionsmanager.saveSetting()

    def loadSetting(self):
        self._optionsmanager.loadSetting()

    def viewData(self):
        self._optionsmanager.viewData()

    def serverConnection(self):
        service = '/singletons/com.sun.star.script.provider.theMasterScriptProviderFactory'
        factory = self._ctx.getByName(service)
        provider = factory.createScriptProvider(self._ctx)
        url = f'vnd.sun.star.script:{g_extension}.{self._module}.{self._sub}?language=Basic&location=application'
        script = provider.getScript(url) 
        try:
            script.invoke(((), ), (), ())
        except Exception as e:
            self._logger.logprb(SEVERE, 'OptionManager', 'serverConnection()', 101, e, traceback.format_exc())
            print("OptionManager.serverConnection() ERROR: %s - %s" % (e, traceback.format_exc()))

    def editMacro(self):
        frame = createService(self._ctx, 'com.sun.star.frame.Frame')
        args = getPropertyValueSet({'Document': 'LibreOffice Macros & Dialogs',
                                    'LibName': g_extension,
                                    'Name': self._module,
                                    'Type': 'Module',
                                    'Line': self._line})
        dispatcher = createService(self._ctx, 'com.sun.star.frame.DispatchHelper')
        dispatcher.executeDispatch(frame, '.uno:BasicIDEAppear', "", 0, args)

