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


public final class DataBase
{
	private XConnection m_xConnection;

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

	public List<Map<String, Object>> getChangedCards() throws SQLException
	{
		XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectChangedCards\"(?,?)");
		XParameters parameters = (XParameters)UnoRuntime.queryInterface(XParameters.class, call);
		parameters.setNull(1, DataType.TIMESTAMP);
		parameters.setNull(2, DataType.TIMESTAMP);
		XResultSet result = call.executeQuery();
		List<Map<String, Object>> maps = _getResult(result);
		_closeCall(call);
		return maps;
	}

	public void updateUser() throws SQLException
	{
		XPreparedStatement call = m_xConnection.prepareCall("CALL \"UpdateUser\"()");
		call.executeUpdate();
		_closeCall(call);
	}

	public List<Map<String, Object>> getAddressbookColumn() throws SQLException
	{
		XPreparedStatement call = m_xConnection.prepareCall("CALL \"SelectAddressbookColumn\"()");
		XResultSet result = call.executeQuery();
		List<Map<String, Object>> maps = _getResult(result);
		_closeCall(call);
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

	private static List<Map<String, Object>> _getResult(XResultSet result) throws SQLException
	{
		System.out.println("DataBase._getResult() 1");
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
			maps.add(map);
		}
		System.out.println("DataBase._getResult() 3");
		return maps;
	}

	private static Object _getValueFromResult(XRow row, String dbtype, int index) throws SQLException
	{
		Object value = null;
		if (dbtype.equals("VARCHAR")) value = row.getString(index);
		else if (dbtype.equals("CHARACTER")) value = row.getString(index);
		else if (dbtype.equals("BOOLEAN")) value = row.getBoolean(index);
		else if (dbtype.equals("TINYINT")) value = row.getByte(index);
		else if (dbtype.equals("SMALLINT")) value = row.getShort(index);
		else if (dbtype.equals("INTEGER")) value = row.getInt(index);
		else if (dbtype.equals("BIGINT")) value = row.getLong(index);
		else if (dbtype.equals("FLOAT")) value = row.getFloat(index);
		else if (dbtype.equals("DOUBLE")) value = row.getDouble(index);
		else if (dbtype.startsWith("TIMESTAMP")) value = row.getTimestamp(index);
		else if (dbtype.equals("TIME")) value = row.getTime(index);
		else if (dbtype.equals("DATE")) value = row.getDate(index);
		else if (dbtype.endsWith("ARRAY")) value = row.getArray(index);
		else System.out.println("DataBase._getValueFromResult() " + dbtype);
		if(row.wasNull()) value = null;
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
