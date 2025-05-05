/*
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
*/
package io.github.prrvchr.carddav;

import java.util.HashMap;
import java.util.Map;

import org.json.JSONObject;

import com.sun.star.beans.NamedValue;
import com.sun.star.sdbc.SQLException;
import com.sun.star.sdbc.XArray;
import com.sun.star.sdbc.XCloseable;
import com.sun.star.sdbc.XConnection;
import com.sun.star.sdbc.XParameters;
import com.sun.star.sdbc.XPreparedStatement;
import com.sun.star.sdbc.XPreparedBatchExecution;
import com.sun.star.sdbc.XResultSet;
import com.sun.star.sdbc.XRow;
import com.sun.star.sdbc.XStatement;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.Type;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.util.DateTimeWithTimezone;

import io.github.prrvchr.uno.helper.Array;
import io.github.prrvchr.uno.helper.UnoHelper;


public final class DataBase
{
    private XConnection m_xConnection;
    private XPreparedBatchExecution m_xCardCall;
    private XPreparedBatchExecution m_xGroupCall;
    private XParameters m_xCardSetting;
    private XParameters m_xGroupSetting;

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
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"GetLastCardSync\"(?)");
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, call);
        call.execute();
        DateTimeWithTimezone timeout = (DateTimeWithTimezone) row.getObject(1, null);
        close(call);
        return timeout;
    }

    public XPreparedStatement getChangedCards(DateTimeWithTimezone start,
                                              DateTimeWithTimezone stop)
        throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, start);
        parameters.setObject(2, stop);
        return call;
    }

    public Map<String, CardProperty> getCardProperties()
    throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectCardProperties\"()");
        XResultSet result = call.executeQuery();
        Map<String, CardProperty> maps = new HashMap<String, CardProperty>();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        while(result != null && result.next()) {
            String name = row.getString(1);
            String getter = row.getString(2);
            boolean isgroup = row.getBoolean(3);
            boolean istyped = row.getBoolean(4);
            XResultSet result2 = row.getArray(5).getResultSet(null);
            XRow row2 = (XRow) UnoRuntime.queryInterface(XRow.class, result2);
            JSONObject methods = new JSONObject();
            while(result2 != null && result2.next()) {
                @SuppressWarnings("unused")
                int i = row2.getInt(1);
                String method = row2.getString(2);
                methods = new JSONObject(methods, method);
            }
            close(result2);
            maps.put(name, new CardProperty(name, getter, isgroup, istyped, methods));
        }
        close(result);
        close(call);
        return maps;
    }

    public boolean prepareBatchCall()
    throws SQLException
    {
        System.out.println("DataBase.prepareBatchCall() 1");
        XArray columns = _getColumnIds();
        if (columns == null) {
            return false;
        }
        _setBatchModeOn();
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"MergeCardData\"(?,?,?,?,?,?,?)");
        m_xCardSetting = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        m_xCardSetting.setArray(1, columns);
        m_xCardSetting.setTimestamp(2, UnoHelper.currentUnoDateTime());
        m_xCardCall = (XPreparedBatchExecution) UnoRuntime.queryInterface(XPreparedBatchExecution.class, call);
        XPreparedStatement call2 = m_xConnection.prepareCall("CALL \"MergeCardGroup\"(?,?)");
        m_xGroupSetting = (XParameters) UnoRuntime.queryInterface(XParameters.class, call2);
        m_xGroupCall = (XPreparedBatchExecution) UnoRuntime.queryInterface(XPreparedBatchExecution.class, call2);
        System.out.println("DataBase.prepareBatchCall() 2");
        return true;
    }

    public XArray _getColumnIds()
    throws SQLException
    {
        System.out.println("DataBase._getColumnIds() 1");
        XArray columns = null;
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectColumnIds\"()");
        XResultSet result = call.executeQuery();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        if(result != null && result.next()) {
            columns = row.getArray(1);
        }
        close(result);
        close(call);
        System.out.println("DataBase._getColumnIds() 2");
        return columns;
    }

    public int mergeCardData(int cid,
                             String prefix,
                             String label,
                             String[] suffixes,
                             String value)
    throws SQLException
    {
        System.out.println("DataBase.mergeCardProperty() CardId: " + cid + " - Prefix: " + prefix + " - Label: " + label);
        m_xCardSetting.setInt(3, cid);
        m_xCardSetting.setString(4, prefix);
        m_xCardSetting.setString(5, label);
        m_xCardSetting.setArray(6, new Array(suffixes, "VARCHAR"));
        m_xCardSetting.setString(7, value);
        m_xCardCall.addBatch();
        return 1;
    }

    public int mergeGroup(int card,
                          int group)
    throws SQLException
    {
        m_xGroupSetting.setInt(1, card);
        m_xGroupSetting.setInt(2, group);
        return 1;
    }

    public void commitBatchCall(int cnum,
                                int gnum,
                                DateTimeWithTimezone timestamp)
    throws SQLException
    {
        System.out.println("DataBase.commitBatchCall() 1");
        if (cnum > 0) {
            m_xCardCall.executeBatch();
        }
        if (gnum > 0) {
            m_xGroupCall.executeBatch();
        }
        m_xConnection.commit();
        _setBatchModeOff();
        close(m_xCardCall);
        close(m_xGroupCall);
        m_xCardCall = null;
        m_xCardSetting = null;
        _updateCardSync(timestamp);
        System.out.println("DataBase.commitBatchCall() 2 Count: " + cnum);
    }

    private void _setBatchModeOn()
        throws SQLException
    {
        XStatement statement = m_xConnection.createStatement();
        _setLoggingChanges(statement, false);
        _saveChanges(statement, false);
        close(statement);
        m_xConnection.setAutoCommit(false);
    }

    private void _setBatchModeOff()
        throws SQLException
    {
        XStatement statement = m_xConnection.createStatement();
        _setLoggingChanges(statement, true);
        _saveChanges(statement, false);
        close(statement);
        m_xConnection.setAutoCommit(true);
    }

    private void _updateCardSync(DateTimeWithTimezone timestamp) throws SQLException
    {
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"UpdateCardSync\"(?)");
        XParameters parameters = (XParameters) UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, timestamp);
        call.executeUpdate();
        close(call);
    }

    private void _setLoggingChanges(XStatement statement, boolean state)
        throws SQLException
    {
        statement.execute(state ? "SET FILES LOG TRUE" : "SET FILES LOG FALSE");
    }

    private void _saveChanges(XStatement statement, boolean compact)
        throws SQLException
    {
        statement.execute(compact ? "CHECKPOINT DEFRAG" : "CHECKPOINT");
    }

    public Map<Integer, JSONObject> getCardGroup()
    throws SQLException
    {
        System.out.println("DataBase.getCardGroup() 1");
        Map<Integer, JSONObject> maps = new HashMap<Integer, JSONObject>();
        XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectCardGroup\"()");
        XResultSet result = call.executeQuery();
        XRow row = (XRow) UnoRuntime.queryInterface(XRow.class, result);
        while(result != null && result.next()) {
            Integer user = row.getInt(1);
            JSONObject groups = new JSONObject();
            for (String group: (String[]) row.getArray(2).getArray(null)) {
                groups = new JSONObject(groups, group);
            }
            maps.put(user, groups);
        }
        close(result);
        close(call);
        System.out.println("DataBase.getCardGroup() 2 Count: " + maps.size());
        return maps;
    }

    public void close(Object object) throws SQLException
    {
        XCloseable closeable = (XCloseable) UnoRuntime.queryInterface(XCloseable.class, object);
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
