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

from com.sun.star.logging.LogLevel import SEVERE

from .optionsmodel import OptionsModel

from .optionsview import OptionsView

from .options import OptionsManager as Manager

from ..unotool import executeDispatch

from ..configuration import g_extension

import traceback


class OptionsManager():
    def __init__(self, ctx, logger, window):
        self._ctx = ctx
        self._model = OptionsModel(ctx)
        self._view = OptionsView(window, OptionsManager._restart, *self._model.getViewData())
        self._manager = Manager(ctx, logger, window)
        self._logger = logger
        self._module = 'CardDAVDiscoveryUrl'
        self._sub = 'Main'
        self._line = 26

    _restart = False

    def saveSetting(self):
        if self._manager.saveSetting():
            print("OptionsManager.saveSetting() restart")
            OptionsManager._restart = True
            self._view.setWarning(True, self._model.isInstrumented())

    def loadSetting(self):
        self._manager.loadSetting()

    def serverConnection(self):
        service = '/singletons/com.sun.star.script.provider.theMasterScriptProviderFactory'
        factory = self._ctx.getByName(service)
        provider = factory.createScriptProvider(self._ctx)
        args = (g_extension, self._module, self._sub)
        url = 'vnd.sun.star.script:%s.%s.%s?language=Basic&location=application' % args
        script = provider.getScript(url)
        try:
            script.invoke(((), ), (), ())
        except Exception as e:
            self._logger.logprb(SEVERE, 'OptionManager', 'serverConnection()', 101, e, traceback.format_exc())
            print("OptionManager.serverConnection() ERROR: %s - %s" % (e, traceback.format_exc()))

    def editMacro(self):
        args = {'Document': 'LibreOffice Macros & Dialogs',
                'LibName': g_extension,
                'Name': self._module,
                'Type': 'Module',
                'Line': self._line}
        executeDispatch(self._ctx, '.uno:BasicIDEAppear', **args)

