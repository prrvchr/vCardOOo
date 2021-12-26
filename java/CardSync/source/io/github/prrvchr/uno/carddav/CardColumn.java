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

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.sun.star.sdbc.SQLException;

import io.github.prrvchr.uno.sdbc.Array;

public final class CardColumn
{

	private String m_property = null;
	private String m_method = null;
	private Boolean m_typed = null;
	private List<String> m_methods = new ArrayList<String>();

	private List<Map<String, Object>> m_columns = new ArrayList<Map<String, Object>>();

	public CardColumn(CardColumn original)
	{
		m_property = original.getProperty();
		m_method = original.getMethod();
		m_typed = original.getTyped();
		m_methods = original.getMethods();
		m_columns = original.getColumns();
	};

	public CardColumn(String property, String method, Boolean typed)
	{
		m_property = property;
		m_method = method;
		m_typed = typed;
	};

	public String getProperty()
	{
		return m_property;
	};

	public String getMethod()
	{
		return m_method;
	};

	public Boolean getTyped()
	{
		return m_typed;
	};
	
	public <U> int getColumnId(List<U> types, String getter)
	throws SQLException, 
		InstantiationException,
		IllegalAccessException, 
		IllegalArgumentException, 
		InvocationTargetException,
		NoSuchMethodException,
		SecurityException
	{
		int id = 0;
		for (Map<String, Object> map: m_columns)
		{
			String method = (String) map.get("ParameterGetter");
			if (getter.equals(method))
			{
				if (types == null)
				{
					id = (int) map.get("ColumnId");
					break;
				}
				else
				{
					@SuppressWarnings("unchecked")
					Class<U> clazz = (Class<U>) types.getClass();
					List<U> type = _getTypes(clazz, map);
					Boolean same = true;
					System.out.println("CardColumn.getColumnId()1 " + types + " - " + type);
					for (U t: types)
					{
						if (!type.contains(t))
						{
							System.out.println("CardColumn.getColumnId()2 " + types + " - " + t);
							same = false;
							break;
						}
					}
					if (same)
					{
						id = (int) map.get("ColumnId");
						System.out.println("CardColumn.getColumnId()3 " + types + " - " + type);
					}
				}
			}
		}
		return id;
	};

	public List<Map<String, Object>> getColumns()
	{
		return new ArrayList<Map<String, Object>>(m_columns);
	}

	public List<String> getMethods()
	{
		return new ArrayList<String>(m_methods);
	};

	public void add(Map<String, Object> map)
	{
		String getter = (String) map.get("ParameterGetter");
		if (!m_methods.contains(getter)) m_methods.add(getter);
		m_columns.add(map);
	};

	private static <U> List<U> _getTypes(Class<U> clazz, Map<String, Object> map)
	throws SQLException,
			InstantiationException,
			IllegalAccessException,
			IllegalArgumentException,
			InvocationTargetException,
			NoSuchMethodException,
			SecurityException
	{
		List<U> types = new ArrayList<U>();
		Object[] object = ((Array) map.get("TypeValues")).getArray(null);
		List<String> list = Stream.of(object).map(Object::toString).collect(Collectors.toList());
		for (String value: list)
		{
			U type = _getInstanceOfT(clazz, value);
			types.add(type);
		}
		return types;
	}

	private static <U> U _getInstanceOfT(Class<U> clazz, String value)
			throws InstantiationException,
					IllegalAccessException,
					IllegalArgumentException,
					InvocationTargetException,
					NoSuchMethodException,
					SecurityException {
        return clazz.getDeclaredConstructor().newInstance(value);
     }
	
	

}
