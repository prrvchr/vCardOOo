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


public final class DataBase {

    private XConnection mConnection;
    private XPreparedBatchExecution mCardCall;
    private XPreparedBatchExecution mGroupCall;
    private XParameters mCardSetting;
    private XParameters mGroupSetting;

    public DataBase(NamedValue[] arguments) {
        this(getConnection(arguments));
    }

    public DataBase(XConnection connection) {
        mConnection = connection;
    }

    public String getUserName() throws SQLException {
        return mConnection.getMetaData().getUserName();
    }

    public String getDriverVersion() throws SQLException {
        return mConnection.getMetaData().getDriverVersion();
    }

    public DateTimeWithTimezone getLastUserSync()
        throws SQLException {
        XPreparedStatement call = mConnection.prepareCall("CALL \"GetLastCardSync\"(?)");
        XRow row = UnoRuntime.queryInterface(XRow.class, call);
        call.execute();
        DateTimeWithTimezone timeout = (DateTimeWithTimezone) row.getObject(1, null);
        close(call);
        return timeout;
    }

    public XPreparedStatement getChangedCards(DateTimeWithTimezone start,
                                              DateTimeWithTimezone stop)
        throws SQLException {
        XPreparedStatement call = mConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
        XParameters parameters = UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, start);
        parameters.setObject(2, stop);
        return call;
    }

    public Map<String, CardProperty> getCardProperties()
        throws SQLException {
        XPreparedStatement call = mConnection.prepareCall("CALL \"SelectCardProperties\"()");
        XResultSet result = call.executeQuery();
        Map<String, CardProperty> maps = new HashMap<String, CardProperty>();
        XRow row = UnoRuntime.queryInterface(XRow.class, result);
        final int NAME = 1;
        final int GETTER = 2;
        final int ISGROUP = 3;
        final int ISTYPED = 4;
        final int VALUES = 5;
        final int INDEX = 1;
        final int VALUE = 2;
        while (result != null && result.next()) {
            String name = row.getString(NAME);
            String getter = row.getString(GETTER);
            boolean isgroup = row.getBoolean(ISGROUP);
            boolean istyped = row.getBoolean(ISTYPED);
            XResultSet result2 = row.getArray(VALUES).getResultSet(null);
            XRow row2 = UnoRuntime.queryInterface(XRow.class, result2);
            JSONObject methods = new JSONObject();
            while (result2 != null && result2.next()) {
                @SuppressWarnings("unused")
                int i = row2.getInt(INDEX);
                String method = row2.getString(VALUE);
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
        throws SQLException {
        boolean batched = false;
        XArray columns = getColumnIds();
        if (columns != null) {
            setBatchModeOn();
            XPreparedStatement call = mConnection.prepareCall("CALL \"MergeCardData\"(?,?,?,?,?,?,?)");
            mCardSetting = UnoRuntime.queryInterface(XParameters.class, call);
            mCardSetting.setArray(1, columns);
            mCardSetting.setTimestamp(2, UnoHelper.currentDateTime());
            mCardCall = UnoRuntime.queryInterface(XPreparedBatchExecution.class, call);
            XPreparedStatement call2 = mConnection.prepareCall("CALL \"MergeCardGroup\"(?,?)");
            mGroupSetting = UnoRuntime.queryInterface(XParameters.class, call2);
            mGroupCall = UnoRuntime.queryInterface(XPreparedBatchExecution.class, call2);
            batched = true;
        }
        return batched;
    }

    public XArray getColumnIds()
        throws SQLException {
        XArray columns = null;
        XPreparedStatement call = mConnection.prepareCall("CALL \"SelectColumnIds\"()");
        XResultSet result = call.executeQuery();
        XRow row = UnoRuntime.queryInterface(XRow.class, result);
        if (result != null && result.next()) {
            columns = row.getArray(1);
        }
        close(result);
        close(call);
        return columns;
    }

    public int mergeCardData(int cid,
                             String prefix,
                             String label,
                             String[] suffixes,
                             String value)
        throws SQLException {
        final int CID = 3;
        final int PREFIX = 4;
        final int LABEL = 5;
        final int SUFFIX = 6;
        final int VALUE = 7;

        mCardSetting.setInt(CID, cid);
        mCardSetting.setString(PREFIX, prefix);
        mCardSetting.setString(LABEL, label);
        mCardSetting.setArray(SUFFIX, new Array(suffixes, "VARCHAR"));
        mCardSetting.setString(VALUE, value);
        mCardCall.addBatch();
        return 1;
    }

    public int mergeGroup(int card,
                          int group)
        throws SQLException {
        mGroupSetting.setInt(1, card);
        mGroupSetting.setInt(2, group);
        return 1;
    }

    public void commitBatchCall(int cnum,
                                int gnum,
                                DateTimeWithTimezone timestamp)
        throws SQLException {
        if (cnum > 0) {
            mCardCall.executeBatch();
        }
        if (gnum > 0) {
            mGroupCall.executeBatch();
        }
        mConnection.commit();
        setBatchModeOff();
        close(mCardCall);
        close(mGroupCall);
        mCardCall = null;
        mCardSetting = null;
        updateCardSync(timestamp);
    }

    private void setBatchModeOn()
        throws SQLException {
        XStatement statement = mConnection.createStatement();
        setLoggingChanges(statement, false);
        saveChanges(statement, false);
        close(statement);
        mConnection.setAutoCommit(false);
    }

    private void setBatchModeOff()
        throws SQLException {
        XStatement statement = mConnection.createStatement();
        setLoggingChanges(statement, true);
        saveChanges(statement, false);
        close(statement);
        mConnection.setAutoCommit(true);
    }

    private void updateCardSync(DateTimeWithTimezone timestamp) throws SQLException {
        XPreparedStatement call = mConnection.prepareCall("CALL \"UpdateCardSync\"(?)");
        XParameters parameters = UnoRuntime.queryInterface(XParameters.class, call);
        parameters.setObject(1, timestamp);
        call.executeUpdate();
        close(call);
    }

    private void setLoggingChanges(XStatement statement, boolean state)
        throws SQLException {
        if (state) {
            statement.execute("SET FILES LOG TRUE");
        } else {
            statement.execute("SET FILES LOG FALSE");
        }
    }

    private void saveChanges(XStatement statement, boolean compact)
        throws SQLException {
        if (compact) {
            statement.execute("CHECKPOINT DEFRAG");
        } else {
            statement.execute("CHECKPOINT");
        }
    }

    public Map<Integer, JSONObject> getCardGroup()
        throws SQLException {
        Map<Integer, JSONObject> maps = new HashMap<Integer, JSONObject>();
        XPreparedStatement call = mConnection.prepareCall("CALL \"SelectCardGroup\"()");
        XResultSet result = call.executeQuery();
        XRow row = UnoRuntime.queryInterface(XRow.class, result);
        while (result != null && result.next()) {
            Integer user = row.getInt(1);
            JSONObject groups = new JSONObject();
            for (String group: (String[]) row.getArray(2).getArray(null)) {
                groups = new JSONObject(groups, group);
            }
            maps.put(user, groups);
        }
        close(result);
        close(call);
        return maps;
    }

    public void close(Object object) throws SQLException {
        XCloseable closeable = UnoRuntime.queryInterface(XCloseable.class, object);
        closeable.close();
    }

    private static XConnection getConnection(NamedValue[] arguments) {
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
