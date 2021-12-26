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
import java.util.List;

import com.sun.star.sdbc.SQLException;

import ezvcard.VCard;
import ezvcard.parameter.VCardParameter;


public final class CardProperty<T>
{

	private List<T> m_properties = null;

	@SuppressWarnings("unchecked")
	public CardProperty(VCard card,
						CardColumn column)
	throws NoSuchMethodException,
			SecurityException,
			IllegalAccessException,
			IllegalArgumentException,
			InvocationTargetException
	{
		m_properties = (List<T>) card.getClass().getDeclaredMethod(column.getMethod()).invoke(card);
	};


	@SuppressWarnings("unchecked")
	public <U> void parse(DataBase database,
							CardColumn columns,
							String query)
	throws NoSuchMethodException,
			SecurityException,
			IllegalAccessException,
			IllegalArgumentException,
			InvocationTargetException,
			SQLException,
			InstantiationException
	{
		System.out.println("CardProperty.parseProperty()1");
		for (T property: m_properties)
		{
			for (String getter: columns.getMethods())
			{
				List<VCardParameter> types = null;
				System.out.println("CardProperty.parseProperty()2 " + getter);
				Object value = property.getClass().getMethod(getter).invoke(property);
				System.out.println("CardProperty.parseProperty()3 " + value);
				if (columns.getTyped())
				{
					types = (List<VCardParameter>) property.getClass().getMethod("getTypes").invoke(property);
					System.out.println("CardProperty.parseProperty()4 " + columns.getTyped() + " - " + types);
				}
				//String name = (String) column.get("ColumnName");
				int id = columns.getColumnId(types, getter);
				System.out.println("CardProperty.parseProperty()5 " + value + " - " + id);
			}
		}
	};
	
}
