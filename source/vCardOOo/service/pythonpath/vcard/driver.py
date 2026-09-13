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

from .card.driver import Driver as DriverBase

from .card.helper import getLogException

from .unotool import getUrl

from .configuration import g_scheme


class Driver(DriverBase):
    def _getConnectionParams(self, url, infos, mtd):
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
        return server, scheme, server, username, password

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
