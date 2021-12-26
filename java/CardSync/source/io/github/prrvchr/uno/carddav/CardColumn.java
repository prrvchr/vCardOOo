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
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.sun.star.sdbc.SQLException;

import ezvcard.parameter.VCardParameter;
import io.github.prrvchr.uno.sdbc.Array;

public final class CardColumn
{

	private String m_property = null;
	private String m_method = null;
	private Boolean m_typed = null;

	private List<String> m_methods = new ArrayList<String>();
	private Map<List<String>, Integer> m_types = new HashMap<List<String>, Integer>();
	private Map<String, Integer> m_ids = new HashMap<String, Integer>();

	public CardColumn(CardColumn original)
	{
		m_property = original.getProperty();
		m_method = original.getMethod();
		m_typed = original.getTyped();
		m_methods = original.getMethods();
		if (m_typed) 
		{
			m_types = original.getTypes();
		}
		else
		{
			m_ids = original.getIds(); 
		}
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

	public Map<List<String>, Integer> getTypes()
	{
		return new HashMap<List<String>, Integer>(m_types);
	};

	public Map<String, Integer> getIds()
	{
		return new HashMap<String, Integer>(m_ids);
	};

	public int getColumnId(List<VCardParameter> types, String getter)
	{
		int id = 0;
		if (m_typed) 
		{
			id = m_types.get(_getTypes(types));
		}
		else
		{
			id = m_ids.get(getter);
		}
		return id;
	};

	public List<String> getMethods()
	{
		return new ArrayList<String>(m_methods);
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
		if (!m_methods.contains(getter)) m_methods.add(getter);
		int id = (int) map.get("ColumnId");
		if (m_typed) 
		{
			m_types.put(_getTypes(map), id);
		}
		else
		{
			m_ids.put(getter, id); 
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
