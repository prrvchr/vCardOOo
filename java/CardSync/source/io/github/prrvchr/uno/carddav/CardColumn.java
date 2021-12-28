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
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.sun.star.sdbc.SQLException;

import ezvcard.parameter.VCardParameter;
import io.github.prrvchr.uno.sdbc.Array;

public final class CardColumn
{

	private String m_property = null;
	private String m_method = null;
	private Short m_type = null;

	private Map<String, Integer> m_methods = new HashMap<String, Integer>();
	private Map<String, Map<List<String>, Integer>> m_types = new HashMap<String, Map<List<String>, Integer>>();

	public CardColumn(CardColumn original)
	{
		m_property = original.getProperty();
		m_method = original.getMethod();
		m_type = original.getType();
		m_methods = original.getMethods();
		if (isTyped()) 
		{
			m_types = original.getTypes();
		}
	};

	public CardColumn(String property, String method, Short type)
	{
		m_property = property;
		m_method = method;
		m_type = type;
	};

	public String getProperty()
	{
		return m_property;
	};

	public String getMethod()
	{
		return m_method;
	};

	public Short getType()
	{
		return m_type;
	};

	public Boolean isTyped()
	{
		return m_type > 1;
	};

	public Boolean isColumn()
	{
		return m_type > 0;
	};

	public Map<String, Map<List<String>, Integer>> getTypes()
	{
		return new HashMap<String, Map<List<String>, Integer>>(m_types);
	};

	public Map<String, Integer> getMethods()
	{
		return new HashMap<String, Integer>(m_methods);
	};

	public Set<String> getGetters()
	{
		return m_methods.keySet();
	};
	
	public int getColumnId(List<VCardParameter> types, String getter)
	{
		int id = 0;
		if (isTyped()) 
		{
			id = m_types.get(getter).get(_getTypes(types));
		}
		else
		{
			id = m_methods.get(getter);
		}
		return id;
	};

	public void add(Map<String, Object> map)
	throws SQLException,
			InstantiationException,
			IllegalAccessException,
			IllegalArgumentException,
			InvocationTargetException,
			NoSuchMethodException,
			SecurityException
	{
		String getter = (String) map.get("ParameterGetter");
		int id = (int) map.get("ColumnId");
		if (!m_methods.containsKey(getter))
		{
			m_methods.put(getter, id);
			if (isTyped()) 
			{
				Map<List<String>, Integer> type = new HashMap<List<String>, Integer>();
				type.put(_getTypes(map), id);
				m_types.put(getter, type);
			}
		}
		else if (isTyped()) 
		{
			m_types.get(getter).put(_getTypes(map), id);
		}
	};

	private static List<String> _getTypes(List<VCardParameter> types)
	{
		List<String> type = new ArrayList<String>();
		for (VCardParameter t: types)
		{
			type.add(t.getValue());
		}
		return type;
	};

	private static List<String> _getTypes(Map<String, Object> map)
	throws SQLException,
			InstantiationException,
			IllegalAccessException,
			IllegalArgumentException,
			InvocationTargetException,
			NoSuchMethodException,
			SecurityException
	{
		Object[] object = ((Array) map.get("TypeValues")).getArray(null);
		List<String> types = Stream.of(object).map(Object::toString).collect(Collectors.toList());
		return types;
	};


}
