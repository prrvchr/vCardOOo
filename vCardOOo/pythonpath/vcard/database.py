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

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from com.sun.star.sdb.CommandType import QUERY

from com.sun.star.sdbc.DataType import INTEGER
from com.sun.star.sdbc.DataType import TIMESTAMP
from com.sun.star.sdbc.DataType import VARCHAR

from .unolib import KeyMap

from .unotool import parseDateTime
from .unotool import createService
from .unotool import getConfiguration
from .unotool import getResourceLocation
from .unotool import getSimpleFile

from .configuration import g_identifier
from .configuration import g_admin
from .configuration import g_group
from .configuration import g_host

from .dbqueries import getSqlQuery

from .dbconfig import g_dba
from .dbconfig import g_folder
from .dbconfig import g_jar
from .dbconfig import g_role
from .dbconfig import g_schema
from .dbconfig import g_user

from .dbtool import Array
from .dbtool import checkDataBase
from .dbtool import createDataSource
from .dbtool import createStaticTable
from .dbtool import getConnectionInfo
from .dbtool import getDataBaseConnection
from .dbtool import getDataBaseUrl
from .dbtool import executeSqlQueries
from .dbtool import getDataFromResult
from .dbtool import getDataSourceCall
from .dbtool import getDataSourceConnection
from .dbtool import executeQueries
from .dbtool import getDictFromResult
from .dbtool import getKeyMapFromResult
from .dbtool import getRowDict
from .dbtool import getSequenceFromResult
from .dbtool import getKeyMapKeyMapFromResult

from .dbinit import getStaticTables
from .dbinit import getQueries
from .dbinit import getTables
from .dbinit import getViews

from .logger import logMessage
from .logger import getMessage

from collections import OrderedDict
import traceback
from time import sleep


class DataBase(unohelper.Base):
    def __init__(self, ctx):
        self._ctx = ctx
        self._statement = None
        self._embedded = False
        self._fieldsMap = {}
        self._batchedCalls = OrderedDict()
        self._addressbook = None
        url = getResourceLocation(ctx, g_identifier, g_folder)
        self._url = url + '/' + g_host
        if self._embedded:
            self._path = url + '/' + g_jar
        else:
            self._path = None
        odb = self._url + '.odb'
        exist = getSimpleFile(ctx).exists(odb)
        if not exist:
            connection = getDataSourceConnection(ctx, self._url)
            error = self._createDataBase(connection)
            if error is None:
                datasource = connection.getParent()
                #datasource.SuppressVersionColumns = True
                datasource.DatabaseDocument.storeAsURL(odb, ())
                datasource.dispose()
            connection.close()

    @property
    def Connection(self):
        if self._statement is None:
            connection = self.getConnection()
            self._statement = connection.createStatement()
        return self._statement.getConnection()

    def getConnection(self, user='', password=''):
        #info = getConnectionInfo(user, password, self._path)
        return getDataSourceConnection(self._ctx, self._url, user, password, False)

    def dispose(self):
        if self._statement is not None:
            connection = self._statement.getConnection()
            self._statement.dispose()
            self._statement = None
            #connection.getParent().dispose()
            connection.close()
            print("gContact.DataBase.dispose() ***************** database: %s closed!!!" % g_host)

# Procedures called by Initialization
    def _createDataBase(self, connection):
        version, error = checkDataBase(self._ctx, connection)
        if error is None:
            statement = connection.createStatement()
            createStaticTable(self._ctx, statement, getStaticTables(), True)
            tables = getTables(self._ctx, connection, version)
            executeSqlQueries(statement, tables)
            executeQueries(self._ctx, statement, getQueries())
            columns = self._getAddressbookColumns(connection)
            views = getViews(self._ctx, columns, self._getViewName())
            executeSqlQueries(statement, views)
            statement.close()
        return error

    def _getAddressbookColumns(self, connection):
        columns = OrderedDict()
        call = getDataSourceCall(self._ctx, connection, 'getAddressbookColumns')
        result = call.executeQuery()
        count = result.MetaData.ColumnCount +1
        while result.next():
            row = getRowDict(result, None, count)
            view = row.get("ViewName")
            if view is not None:
                if view not in columns:
                    columns[view] = OrderedDict()
                columns[view][row.get("ColumnName")] = row.get("ColumnId")
        call.close()
        return columns

    def getDataSource(self):
        return self.Connection.getParent()

    def getDatabaseDocument(self):
        return self.getDataSource().DatabaseDocument

    def addCloseListener(self, listener):
        datasource = self.Connection.getParent()
        document = datasource.DatabaseDocument
        document.addCloseListener(listener)

    def shutdownDataBase(self, compact=False):
        statement = self.Connection.createStatement()
        query = getSqlQuery(self._ctx, 'shutdown', compact)
        statement.execute(query)
        statement.close()

    def createUser(self, user, password):
        statement = self.Connection.createStatement()
        format = {'User': g_user % user,
                  'Password': password,
                  'Admin': g_admin}
        query = getSqlQuery(self._ctx, 'createUser', format)
        status = statement.executeUpdate(query)
        statement.close()
        return status == 0

    def createUserSchema(self, user):
        view = self._getViewName()
        format = {'Schema': g_schema % user,
                  'Public': 'PUBLIC',
                  'User': g_user % user,
                  'View': view,
                  'Name': view,
                  'OldName': view}
        statement = self.Connection.createStatement()
        query = getSqlQuery(self._ctx, 'createUserSchema', format)
        statement.execute(query)
        query = getSqlQuery(self._ctx, 'setUserSchema', format)
        statement.execute(query)
        self._deleteUserView(statement, format)
        self._createUserView(statement, 'createDefaultAddressbookView', format)
        statement.close()

    def selectUser(self, server, name):
        user = None
        call = self._getCall('selectUser')
        call.setString(1, server)
        call.setString(2, name)
        result = call.executeQuery()
        if result.next():
            user = getKeyMapFromResult(result)
        call.close()
        return user

    def selectChangedAddressbooks(self):
        addressbooks = []
        call = self._getCall('selectChangedAddressbooks')
        call.setNull(1, TIMESTAMP)
        call.setNull(2, TIMESTAMP)
        result = call.executeQuery()
        while result.next():
            addressbooks.append(getDataFromResult(result))
        call.close()
        return addressbooks

    def setChangedAddressbook(self):
        call = self._getCall('updateAddressbook')
        status = call.executeUpdate()
        call.close()

    def selectChangedGroups(self):
        groups = []
        call = self._getCall('selectChangedGroups')
        call.setNull(1, TIMESTAMP)
        call.setNull(2, TIMESTAMP)
        result = call.executeQuery()
        while result.next():
            groups.append(getDataFromResult(result))
        call.close()
        return groups

    def setChangedGroup(self):
        call = self._getCall('updateGroup')
        status = call.executeUpdate()
        call.close()

    def initUserAddressbookView(self, format):
        statement = self.Connection.createStatement()
        query = format.get('Query')
        format['Public'] = 'PUBLIC'
        format['View'] = self._getViewName()
        if query == 'Deleted':
            self._deleteUserView(statement, format)
        elif query == 'Inserted':
            self._createUserView(statement, 'createAddressbookView', format)
        elif query == 'Updated':
            self._deleteUserView(statement, format)
            self._createUserView(statement, 'createAddressbookView', format)
        statement.close()

    def initUserGroupView(self, format):
        statement = self.Connection.createStatement()
        query = format.get('Query')
        format['Public'] = 'PUBLIC'
        format['View'] = self._getViewName()
        if query == 'Deleted':
            self._deleteUserView(statement, format)
        elif query == 'Inserted':
            self._createUserView(statement, 'createGroupView', format)
        elif query == 'Updated':
            self._deleteUserView(statement, format)
            self._createUserView(statement, 'createGroupView', format)
        statement.close()

    def _createUserView(self, statement, view, format):
        query = getSqlQuery(self._ctx, view, format)
        print("DataBase._createUserView() 1: %s\n%s" % (view, query))
        statement.execute(query)

    def _deleteUserView(self, statement, format):
        query = getSqlQuery(self._ctx, 'deleteView', format)
        print("DataBase._deleteUserView() 1: %s" % (query, ))
        statement.execute(query)

    def selectAddressbook(self, uid, aid, name):
        addressbook = None
        call = self._getCall('selectAddressbook')
        call.setInt(1, uid)
        if aid is None:
            call.setNull(2, INTEGER)
        else:
            call.setInt(2, aid)
        if name:
            call.setString(3, name)
        else:
            call.setNull(3, VARCHAR)
        result = call.executeQuery()
        if result.next():
            addressbook = getKeyMapFromResult(result)
        call.close()
        return addressbook

    def insertUser(self, scheme, server, path, name):
        user = None
        call = self._getCall('insertUser')
        call.setString(1, scheme)
        call.setString(2, server)
        call.setString(3, path)
        call.setString(4, name)
        result = call.executeQuery()
        if result.next():
            user = getKeyMapFromResult(result)
        call.close()
        return user

    def insertAddressbook(self, user, path, name, tag, token):
        addressbook = None
        call = self._getCall('insertAddressbook')
        call.setInt(1, user)
        call.setString(2, path)
        call.setString(3, name)
        if tag:
            call.setString(4, tag)
        else:
            call.setNull(4, VARCHAR)
        if token:
            call.setString(5, token)
        else:
            call.setNull(5, VARCHAR)
        state = call.executeUpdate()
        addressbook = call.getInt(6)
        call.close()
        return addressbook

    def updateAddressbookName(self, addressbook, name):
        call = self._getCall('updateAddressbookName')
        call.setInt(1, addressbook)
        call.setString(2, name)
        state = call.executeUpdate()
        call.close()

    def updateAddressbookToken(self, aid, token):
        call = self._getCall('updateAddressbookToken')
        call.setString(1, token)
        call.setInt(2, aid)
        state = call.executeUpdate()
        call.close()

# Procedures called by the User


# Procedures called by the Replicator
    def mergeCard(self, aid, path, etag, data):
        call = self._getBatchedCall('mergeCard')
        call.setInt(1, aid)
        call.setString(2, path)
        call.setString(3, etag)
        call.setString(4, data)
        call.addBatch()
        return 1

    def deleteCard(self, aid, urls):
        array = Array('VARCHAR', urls)
        call = self._getCall('deleteCard')
        call.setInt(1, aid)
        call.setArray(2, array)
        status = call.executeUpdate()
        print("DataBase.deleteCard() %s" % status)
        call.close()
        return len(urls)




    def getDefaultType(self):
        default = {}
        call = self._getCall('getDefaultType')
        result = call.executeQuery()
        default = getDictFromResult(result)
        call.close()
        return default

    def setLoggingChanges(self, state):
        statement = self.Connection.createStatement()
        query = getSqlQuery(self._ctx, 'loggingChanges', state)
        statement.execute(query)
        statement.close()

    def saveChanges(self, compact=False):
        statement = self.Connection.createStatement()
        query = getSqlQuery(self._ctx, 'saveChanges', compact)
        statement.execute(query)
        statement.close()

    def getUpdatedGroups(self, user, prefix):
        groups = None
        call = self._getCall('selectUpdatedGroup')
        call.setString(1, prefix)
        call.setLong(2, user.People)
        call.setString(3, user.Resource)
        result = call.executeQuery()
        groups = getKeyMapKeyMapFromResult(result)
        call.close()
        return groups

    def updateSyncToken(self, user, token, data, timestamp):
        value = data.getValue(token)
        call = self._getBatchedCall('update%s' % token)
        call.setString(1, value)
        call.setTimestamp(2, timestamp)
        call.setLong(3, user.People)
        call.addBatch()
        return KeyMap(**{token: value})

    def mergePeople(self, user, resource, timestamp, deleted):
        call = self._getBatchedCall('mergePeople')
        call.setString(1, 'people/')
        call.setString(2, resource)
        call.setLong(3, user.Group)
        call.setTimestamp(4, timestamp)
        call.setBoolean(5, deleted)
        call.addBatch()
        return (0, 1) if deleted else (1, 0)

    def mergePeopleData(self, table, resource, typename, label, value, timestamp):
        format = {'Table': table, 'Type': typename}
        call = self._getBatchedCall(table, 'mergePeopleData', format)
        call.setString(1, 'people/')
        call.setString(2, resource)
        call.setString(3, label)
        call.setString(4, value)
        call.setTimestamp(5, timestamp)
        if typename is not None:
            call.setString(6, table)
            call.setString(7, typename)
        call.addBatch()
        return 1

    def mergeGroup(self, user, resource, name, timestamp, deleted):
        call = self._getBatchedCall('mergeGroup')
        call.setString(1, 'contactGroups/')
        call.setLong(2, user.People)
        call.setString(3, resource)
        call.setString(4, name)
        call.setTimestamp(5, timestamp)
        call.setBoolean(6, deleted)
        call.addBatch()
        return (0, 1) if deleted else (1, 0)

    def mergeConnection(self, user, data, timestamp):
        separator = ','
        call = self._getBatchedCall('mergeConnection')
        call.setString(1, 'contactGroups/')
        call.setString(2, 'people/')
        call.setString(3, data.getValue('Resource'))
        call.setTimestamp(4, timestamp)
        call.setString(5, separator)
        members = data.getDefaultValue('Connections', ())
        call.setString(6, separator.join(members))
        call.addBatch()
        print("DataBase._mergeConnection() %s - %s" % (data.getValue('Resource'), len(members)))
        return len(members)

    def executeBatchCall(self):
        for name in self._batchedCalls:
            call = self._batchedCalls[name]
            call.executeBatch()
            call.close()
        self._batchedCalls = OrderedDict()

# Procedures called internaly
    def _encodePassword(self, password):
        return uno.sequence(password)

    def _escapeQuote(self, text):
        return text.replace("'", "''")

    def _getViewName(self):
        if self._addressbook is None:
            configuration = getConfiguration(self._ctx, g_identifier, False)
            self._addressbook = configuration.getByName('AddressBookName')
        return self._addressbook

    def _getCall(self, name, format=None):
        return getDataSourceCall(self._ctx, self.Connection, name, format)

    def _getBatchedCall(self, key, name=None, format=None):
        if key not in self._batchedCalls:
            name = key if name is None else name
            self._batchedCalls[key] = getDataSourceCall(self._ctx, self.Connection, name, format)
        return self._batchedCalls[key]

    def _getPreparedCall(self, name):
        # TODO: cannot use: call = self.Connection.prepareCommand(name, QUERY)
        # TODO: it trow a: java.lang.IncompatibleClassChangeError
        #query = self.Connection.getQueries().getByName(name).Command
        #self._CallsPool[name] = self.Connection.prepareCall(query)
        return self.Connection.prepareCommand(name, QUERY)
