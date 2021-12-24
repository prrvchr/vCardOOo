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
import java.util.List;
import java.util.Map;

public final class CardColumn
{

	private String m_property = null;
	private String m_method = null;
	private List<Map<String, Object>> m_columns = new ArrayList<Map<String, Object>>();

	public CardColumn(CardColumn original)
	{
		m_property = original.getProperty();
		m_method = original.getMethod();
		m_columns = original.getColumns();
	};
	
	public CardColumn(String property, String method)
	{
		m_property = property;
		m_method = method;
	};

	public String getProperty()
	{
		return m_property;
	};

	public String getMethod()
	{
		return m_method;
	};
	
	public List<Map<String, Object>> getColumns()
	{
		return new ArrayList<Map<String, Object>>(m_columns);
	};

	public void add(Map<String, Object> map)
	{
		m_columns.add(map);
	};
	
}
