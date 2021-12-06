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
package io.github.prrvchr.uno.carddav;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.sun.star.sdbc.SQLException;
import com.sun.star.sdbc.XCloseable;
import com.sun.star.sdbc.XConnection;
import com.sun.star.sdbc.XParameters;
import com.sun.star.sdbc.XPreparedStatement;
import com.sun.star.sdbc.XResultSet;
import com.sun.star.sdbc.XResultSetMetaDataSupplier;
import com.sun.star.sdbc.XRow;
import com.sun.star.util.DateTime;


public final class DataBase
{
	private final XConnection m_xConnection;

	public DataBase(XConnection connection)
	{
		m_xConnection = connection;
	};

	public String getUserName() throws SQLException
	{
		return m_xConnection.getMetaData().getUserName();
	}

	public String getDriverVersion() throws SQLException
	{
		return m_xConnection.getMetaData().getDriverVersion();
	}

	public List<Map<String, Object>> getChangedCards(DateTime first, DateTime last) throws SQLException
	{
		System.out.println("CardSync.getChangedCards() 1");
		XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
		XParameters parameters = (XParameters) call;
		parameters.setTimestamp(1, first);
		parameters.setTimestamp(2, last);
		XResultSet result = call.executeQuery();
		System.out.println("CardSync.getChangedCards() 2");
		List<Map<String, Object>>maps = _getResult(result);
		_closeCall(call);
		System.out.println("CardSync.getChangedCards() 3");
		return maps;
	}

	private static List<Map<String, Object>> _getResult(XResultSet result) throws SQLException
	{
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier) result;
		int len = metadata.getMetaData().getColumnCount();
		XRow row = (XRow) result;
		while(result.next())
		{
			Map<String, Object> map = new HashMap<String, Object>();
			for (int i = 1; i <= len; i++)
			{
				String dbtype = metadata.getMetaData().getColumnTypeName(i);
				map.put(metadata.getMetaData().getColumnLabel(i), _getValueFromResult(row, dbtype, i));
			}
			maps.add(map);
		}
		return maps;
	}

	private static Object _getValueFromResult(XRow row, String dbtype, int index)
	{
		// TODO: 'TINYINT' is buggy: don't use it
		Object value = null;
		try
		{
			if (dbtype == "VARCHAR")
			{
				value = row.getString(index);
			}
			else if (dbtype == "BOOLEAN")
			{
				value = row.getBoolean(index);
			}
			else if (dbtype == "TINYINT"){
				value = row.getShort(index);
			}
			else if (dbtype == "SMALLINT"){
				value = row.getShort(index);
			}
			else if (dbtype == "INTEGER"){
				value = row.getInt(index);
			}
			else if (dbtype == "BIGINT"){
				value = row.getLong(index);
			}
			else if (dbtype == "FLOAT"){
				value = row.getFloat(index);
			}
			else if (dbtype == "DOUBLE"){
				value = row.getDouble(index);
			}
			else if (dbtype == "TIMESTAMP"){
				value = row.getTimestamp(index);
			}
			else if (dbtype == "TIME"){
				value = row.getTime(index);
			}
			else if (dbtype == "DATE"){
				value = row.getDate(index);
			}
		}
		catch (SQLException e) {e.getStackTrace();}
		return value;
	}

	private static void _closeCall(XPreparedStatement call) throws SQLException
	{
		XCloseable closeable = (XCloseable) call;
		closeable.close();
	}


}
