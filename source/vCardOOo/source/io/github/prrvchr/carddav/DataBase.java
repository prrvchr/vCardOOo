/*
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
*/
package io.github.prrvchr.carddav;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.sun.star.beans.NamedValue;
import com.sun.star.sdbc.DataType;
import com.sun.star.sdbc.SQLException;
import com.sun.star.sdbc.XCloseable;
import com.sun.star.sdbc.XConnection;
import com.sun.star.sdbc.XParameters;
import com.sun.star.sdbc.XPreparedStatement;
import com.sun.star.sdbc.XResultSet;
import com.sun.star.sdbc.XResultSetMetaDataSupplier;
import com.sun.star.sdbc.XRow;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.Type;
import com.sun.star.uno.UnoRuntime;

import io.github.prrvchr.css.util.DateTimeWithTimezone;
import io.github.prrvchr.uno.helper.Array;
import io.github.prrvchr.uno.helper.UnoHelper;


public final class DataBase
{
    private XConnection m_xConnection;

    public DataBase(NamedValue[] arguments)
    {
        this(_getConnection(arguments));
    }

    public DataBase(XConnection connection)
    {
        m_xConnection = connection;
    }

    public String getUserName() throws SQLException
    {
        return m_xConnection.getMetaData().getUserName();
    }

    public String getDriverVersion() throws SQLException
    {
        return m_xConnection.getMetaData().getDriverVersion();
    }


    public DateTimeWithTimezone getLastUserSync()
        throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"GetLastUserSync\"()");
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, call);
        call.execute();
        DateTimeWithTimezone timeout = (DateTimeWithTimezone) row.getObject(1, null);
        _closeCall(call);
        return timeout;
    }

    public List<Map<String, Object>> getChangedCards(DateTimeWithTimezone start,
                                                     DateTimeWithTimezone stop)
        throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, start);
        parameters.setObject(2, stop);
        XResultSet result = call.executeQuery();
        List<Map<String, Object>> maps = _getChangedCards(result);
        _closeCall(call);
        System.out.println("DataBase.getChangedCards() Count: " + maps.size());
        return maps;
    }

    public void updateUser(DateTimeWithTimezone timestamp) throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"UpdateUser\"(?)");
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, timestamp);
        call.executeUpdate();
        _closeCall(call);
    }

    public Map<String, CardColumn> getAddressbookColumn()
    throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectAddressbookColumns\"()");
        XResultSet result = call.executeQuery();
        Map<String, CardColumn> maps = _getAddressbookColumn(result, "PropertyName", "PropertyGetter", "Method");
        _closeCall(call);
        return maps;
    }

    public Map<Integer, CardGroup> getCardGroup()
    throws SQLException
    {
        System.out.println("DataBase.getCardGroup() 1");
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectCardGroup\"()");
        XResultSet result = call.executeQuery();
        Map<Integer,  CardGroup> maps = _getCardGroup(result, "User", "Names", "Groups");
        _closeCall(call);
        System.out.println("DataBase.getCardGroup() 2");
        return maps;
    }

    public Integer insertGroup(int user,
                               String group)
    throws SQLException
    {
        Integer id = null;
        String query = "CALL \"InsertGroup\"(?,?,?)";
        System.out.println("DataBase.insertGroup() UserdId: " + user + " - Group: " + group);
        XPreparedStatement call = m_xConnection.prepareCall(query);
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setInt(1, user);
        parameters.setString(2, group);
        call.executeUpdate();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, call);
        id = row.getInt(3);
        _closeCall(call);
        return id;
    }


    public void mergeGroup(int card,
                           Object[] groups)
    throws SQLException
    {
        String query = "CALL \"MergeCardGroup\"(?,?)";
        System.out.println("DataBase.mergeGroup() CardId: " + card + " - Group: " + groups);
        XPreparedStatement call = m_xConnection.prepareCall(query);
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setInt(1, card);
        parameters.setArray(2, new Array(groups, "INTEGER"));
        call.executeUpdate();
        _closeCall(call);
    }

    public void parseCard(int card,
                          int column,
                          String value)
    throws SQLException
    {
        String query = "CALL \"MergeCardValue\"(?,?,?)";
        System.out.println("DataBase.parseCard() CardId: " + card + " - ColumnId: " + column + " - Value: " + value);
        XPreparedStatement call = m_xConnection.prepareCall(query);
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setInt(1, card);
        parameters.setInt(2, column);
        if (value == null) {
            parameters.setNull(3, DataType.VARCHAR);
        }
        else {
            parameters.setString(3, value);
        }
        call.executeUpdate();
        _closeCall(call);
    }

    private static List<Map<String, Object>> _getChangedCards(XResultSet result) throws SQLException
    {
        System.out.println("DataBase._getChangedCards() 1");
        List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
        XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier) UnoRuntime.queryInterface(XResultSetMetaDataSupplier.class, result);
        int len = metadata.getMetaData().getColumnCount();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        while(result != null && result.next()) {
            maps.add(_getRowMap(metadata, row, len));
        }
        System.out.println("DataBase._getChangedCards() 2 Card Count: " + maps.size());
        return maps;
    }

    private static Map<Integer, CardGroup> _getCardGroup(XResultSet result,
                                                         String key,
                                                         String name,
                                                         String group)
    throws SQLException
    {
        Map<Integer, CardGroup> maps = new HashMap<Integer, CardGroup>();
        XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier) UnoRuntime.queryInterface(XResultSetMetaDataSupplier.class, result);
        int len = metadata.getMetaData().getColumnCount();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        while(result != null && result.next()) {
            CardGroup groups = new CardGroup(_getRowMap(metadata, row, len), key, name, group);
            maps.put(groups.getUser(), groups);
        }
        return maps;
    }

    private static Map<String, CardColumn> _getAddressbookColumn(XResultSet result, String key, String getter, String method) 
    throws SQLException
    {
        String mapkey = null;
        CardColumn column = null;
        Map<String, CardColumn> maps = new HashMap<String, CardColumn>();
        XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier) UnoRuntime.queryInterface(XResultSetMetaDataSupplier.class, result);
        int len = metadata.getMetaData().getColumnCount();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        while(result != null && result.next()) {
            Map<String, Object> map = _getRowMap(metadata, row, len);
            if (mapkey == null || !mapkey.equals(map.get(key))) {
                if (mapkey != null) maps.put(mapkey, new CardColumn(column));
                mapkey = (String) map.get(key);
                column = new CardColumn(mapkey, (String) map.get(getter), (Short) map.get(method));
            }
            column.add(map);
        }
        if (column != null) maps.put(mapkey, new CardColumn(column));
        return maps;
    }

    private static Map<String, Object> _getRowMap(XResultSetMetaDataSupplier metadata, XRow row, int len) throws SQLException
    {
        return  _getRowMap(metadata, row, 1, len);
    }
    
    private static Map<String, Object> _getRowMap(XResultSetMetaDataSupplier metadata, XRow row, int start, int len) throws SQLException
    {
        Map<String, Object> map = new HashMap<String, Object>();
        for (int i = 1; i <= len; i++) {
            String name = metadata.getMetaData().getColumnLabel(i);
            int dbtype = metadata.getMetaData().getColumnType(i);
            map.put(name, UnoHelper.getRowValue(row, dbtype, i));
        }
        return map;
    }

    private static void _closeCall(XPreparedStatement call) throws SQLException
    {
        XCloseable closeable = (XCloseable) UnoRuntime.queryInterface(XCloseable.class, call);
        closeable.close();
    }

    private static XConnection _getConnection(NamedValue[] arguments)
    {
        XConnection connection = null;
        for (NamedValue argument: arguments) {
            if (argument.Name.equals("DynamicData")) {
                NamedValue[] values = (NamedValue[]) AnyConverter.toArray(argument.Value);
                for (NamedValue value: values) {
                    if (value.Name.equals("Connection")) {
                        connection = (XConnection) AnyConverter.toObject(new Type(XConnection.class), value.Value);
                        break;
                    }
                }
                break;
            }
        }
        return connection;
    }


}
