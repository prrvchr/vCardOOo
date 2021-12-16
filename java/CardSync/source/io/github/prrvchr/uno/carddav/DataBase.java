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


import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.sun.star.beans.NamedValue;
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
import com.sun.star.util.DateTime;

import io.github.prrvchr.uno.helper.UnoHelper;


public final class DataBase
{
	private XConnection m_xConnection;
	private DateTime m_timestamp;

	public DataBase(NamedValue[] arguments)
	{
		this(_getConnection(arguments));
	};

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

	private DateTime _getTimestamp() throws SQLException
	{
		DateTime timestamp = new DateTime();
		String query = "SELECT \"Modified\" FROM \"Users\" WHERE \"User\"=?";
		XPreparedStatement call = m_xConnection.prepareStatement(query);
		XParameters parameters = (XParameters)UnoRuntime.queryInterface(XParameters.class, call);
		parameters.setInt(1, 0);
		XResultSet result = call.executeQuery();
		if(result != null && result.next())
		{
			XRow row = (XRow)UnoRuntime.queryInterface(XRow.class, result);
			timestamp = row.getTimestamp(1);
		}
		return timestamp;
	}
	
	public void setTimestamp() throws SQLException
	{
		String query = "UPDATE \"Users\" SET \"Modified\"=? WHERE \"User\"=?";
		XPreparedStatement call = m_xConnection.prepareStatement(query);
		XParameters parameters = (XParameters)UnoRuntime.queryInterface(XParameters.class, call);
		parameters.setTimestamp(1, m_timestamp);
		parameters.setInt(2, 0);
		call.executeUpdate();
	}

	public List<Map<String, Object>> getChangedCards() throws SQLException
	{
		System.out.println("DataBase.getChangedCards() 1");
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		try
		{
			String query = "CALL \"UpdateUser\"()";
			XPreparedStatement call = m_xConnection.prepareStatement(query);
			call.executeUpdate();
			_closeCall(call);
			query = "DECLARE FIRST, LAST TIMESTAMP(6) WITH TIME ZONE;\n"
				+ "SET (FIRST, LAST) = (SELECT \"Created\", \"Modified\" FROM \"Users\" WHERE \"User\"=0);\n"
				+ "CALL \"SelectChangedCards\"(FIRST, LAST)";
			call = m_xConnection.prepareStatement(query);
			XResultSet result = call.executeQuery();
			System.out.println("DataBase.getChangedCards() 2");
			maps = _getResult(result);
			_closeCall(call);
			System.out.println("DataBase.getChangedCards() 3");
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("DataBase.getChangedCards() 7");
		return maps;
	}



	public List<Map<String, Object>> getChangedCards1() throws SQLException
	{
		DateTime first = _getTimestamp();
		DateTime last = UnoHelper.getUnoDateTime(Timestamp.valueOf(LocalDateTime.now()));
		printTimestamp("DataBase", "getChangedCards", 1, first);
		printTimestamp("DataBase", "getChangedCards", 2, last);
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		try
		{
			XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
			XParameters parameters = (XParameters)UnoRuntime.queryInterface(XParameters.class, call);
			System.out.println("DataBase.getChangedCards() 3");
			parameters.setTimestamp(1, first);
			parameters.setTimestamp(2, last);
			XResultSet result = call.executeQuery();
			System.out.println("DataBase.getChangedCards() 4");
			XRow row = (XRow)UnoRuntime.queryInterface(XRow.class, call);
			first = row.getTimestamp(1);
			printTimestamp("DataBase", "getChangedCards", 5, first);
			m_timestamp = row.getTimestamp(2);
			printTimestamp("DataBase", "getChangedCards", 6, m_timestamp);
			maps = _getResult(result);
			_closeCall(call);
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("DataBase.getChangedCards() 7");
		return maps;
	}

	public void printTimestamp(String clazz, String method, int num, DateTime timestamp)
	{
		System.out.println(clazz + "." + method + "() " + num + " Timestamp: " + timestamp.Year + "-" + timestamp.Month + "-" + timestamp.Day + "T" + timestamp.Hours + ":" + timestamp.Minutes + ":" + timestamp.Seconds + "." + timestamp.NanoSeconds + "Z");
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

	private static DateTimeFormatter _getDateTimeFormatter()
	{
		return DateTimeFormatter.ofPattern("uuuu-MM-dd HH:mm:ss.nXXX");
	}

	private static List<Map<String, Object>> _getResult(XResultSet result) throws SQLException
	{
		System.out.println("DataBase._getResult() 1");
		int j = 0;
		List<Map<String, Object>> maps = new ArrayList<Map<String, Object>>();
		XResultSetMetaDataSupplier metadata = (XResultSetMetaDataSupplier)UnoRuntime.queryInterface(XResultSetMetaDataSupplier.class, result);
		int len = metadata.getMetaData().getColumnCount();
		XRow row = (XRow)UnoRuntime.queryInterface(XRow.class, result);
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

	private static XConnection _getConnection(NamedValue[] arguments)
	{
		XConnection connection = null;
		for (NamedValue argument: arguments)
		{
			if (argument.Name.equals("DynamicData"))
			{
				NamedValue[] values = (NamedValue[]) AnyConverter.toArray(argument.Value);
				for (NamedValue value: values)
				{
					if (value.Name.equals("Connection"))
					{
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
