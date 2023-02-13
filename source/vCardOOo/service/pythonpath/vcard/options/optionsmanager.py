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

import unohelper

from .optionsmodel import OptionsModel
from .optionsview import OptionsView

from ..unotool import getDesktop

from ..logger import LogManager

import os
import sys
import traceback


class OptionsManager(unohelper.Base):
    def __init__(self, ctx):
        self._ctx = ctx
        self._model = OptionsModel(ctx)
        self._view = None
        self._logger = None

    def initialize(self, window):
        timeout = self._model.getTimeout()
        enabled = self._model.hasDatasource()
        self._view = OptionsView(window, timeout, enabled)
        version  = ' '.join(sys.version.split())
        path = os.pathsep.join(sys.path)
        loggers = {'Driver': True, 'Replicator': True}
        infos = {111: version, 112: path}
        self._logger = LogManager(self._ctx, window.Peer, loggers, infos)

    def saveSetting(self):
        timeout = self._view.getTimeout()
        self._model.setTimeout(timeout)
        self._logger.saveLoggerSetting()

    def reloadSetting(self):
        timeout = self._model.getTimeout()
        self._view.setTimeout(timeout)
        self._logger.setLoggerSetting()

    def viewData(self):
        url = self._model.getDatasourceUrl()
        getDesktop(self._ctx).loadComponentFromURL(url, '_default', 0, ())
