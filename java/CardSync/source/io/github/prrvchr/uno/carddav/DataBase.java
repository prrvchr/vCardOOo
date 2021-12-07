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
import com.sun.star.uno.UnoRuntime;
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
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		try
		{
			System.out.println("DataBase.getChangedCards() 1");
			XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
			System.out.println("DataBase.getChangedCards() 2");
			XParameters parameters = (XParameters)UnoRuntime.queryInterface(XParameters.class, call);
			System.out.println("DataBase.getChangedCards() 3");
			parameters.setTimestamp(1, first);
			parameters.setTimestamp(2, last);
			XResultSet result = call.executeQuery();
			System.out.println("DataBase.getChangedCards() 4");
			XRow row = (XRow)UnoRuntime.queryInterface(XRow.class, result);
			DateTime updated = row.getTimestamp(3);
			System.out.println("DataBase.getChangedCards() 5 " + updated);
			maps = _getResult(result, row);
			_closeCall(call);
			System.out.println("DataBase.getChangedCards() 6 " + updated);
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		return maps;
	}

	public int deleteCard(int id)
	{
		return 1;
	}

	public int insertCard(int id)
	{
		return 1;
	}

	public int updateCard(int id)
	{
		return 1;
	}

	private static List<Map<String, Object>> _getResult(XResultSet result, XRow row) throws SQLException
	{
		System.out.println("DataBase._getResult() 1");
		int j = 0;
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier)UnoRuntime.queryInterface(XResultSetMetaDataSupplier.class, result);
		int len = metadata.getMetaData().getColumnCount();
		while(result != null && result.next())
		{
			Map<String, Object> map = new HashMap<String, Object>();
			for (int i = 1; i <= len; i++)
			{
				String name = metadata.getMetaData().getColumnLabel(i);
				String dbtype = metadata.getMetaData().getColumnTypeName(i);
				Object value = _getValueFromResult(row, dbtype, i);
				map.put(name, value);
				System.out.println("DataBase._getResult() 2: Name: " + name + " - Type: " + dbtype);
			}
			maps.add(j, map);
			j++;
			
			System.out.println("DataBase._getResult() 3");
		}
		System.out.println("DataBase._getResult() 4");
		return maps;
	}

	private static Object _getValueFromResult(XRow row, String dbtype, int index)
	{
		// TODO: 'TINYINT' is buggy: don't use it
		Object value = null;
		try
		{
			if (dbtype.equals("VARCHAR"))
			{
				value = row.getString(index);
			}
			else if (dbtype.equals("CHARACTER"))
			{
				value = row.getString(index);
			}
			else if (dbtype.equals("BOOLEAN"))
			{
				value = row.getBoolean(index);
			}
			else if (dbtype.equals("TINYINT"))
			{
				value = row.getShort(index);
			}
			else if (dbtype.equals("SMALLINT"))
			{
				value = row.getShort(index);
			}
			else if (dbtype.equals("INTEGER"))
			{
				value = row.getInt(index);
			}
			else if (dbtype.equals("BIGINT"))
			{
				value = row.getLong(index);
			}
			else if (dbtype.equals("FLOAT"))
			{
				value = row.getFloat(index);
			}
			else if (dbtype.equals("DOUBLE"))
			{
				value = row.getDouble(index);
			}
			else if (dbtype.startsWith("TIMESTAMP"))
			{
				value = row.getTimestamp(index);
			}
			else if (dbtype.equals("TIME"))
			{
				value = row.getTime(index);
			}
			else if (dbtype.equals("DATE"))
			{
				value = row.getDate(index);
			}
			if(row.wasNull())
			{
				value = null;
			}
		}
		catch (SQLException e) {e.getStackTrace();}
		return value;
	}

	private static void _closeCall(XPreparedStatement call) throws SQLException
	{
		XCloseable closeable = (XCloseable)UnoRuntime.queryInterface(XCloseable.class, call);
		closeable.close();
	}


}
