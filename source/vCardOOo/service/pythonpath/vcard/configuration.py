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

# General configuration
g_extension = 'vCardOOo'
g_identifier = 'io.github.prrvchr.%s' % g_extension
g_protocol = 'sdbc:address:vcard'
g_implementation = '%s.Driver' % g_identifier

# Resource strings files folder
g_resource = 'resource'
g_basename = 'Driver'

g_defaultlog = 'vCardLog'
g_errorlog = 'vCardError'
g_synclog = 'vCardSync'

g_scheme = 'https://'
g_host = 'nextcloud'

g_page = 100
g_member = 1000
g_admin = False
g_compact = 100

g_group = 'all'
g_filter = 'USER_CONTACT_GROUP'
g_timestamp = '%Y-%m-%dT%H:%M:%S.00'
g_db_timestamp = 'YYYY-MM-DD"T"HH24:MI:SS.FFFFFFFFFFFF"Z"'
