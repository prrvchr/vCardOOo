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
import java.lang.reflect.Method;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

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
							int id,
							CardColumn columns,
							String name)
	throws IllegalAccessException, 
	IllegalArgumentException,
	InvocationTargetException,
	NoSuchMethodException, 
	SecurityException, 
	SQLException
	{
		for (T property: m_properties)
		{
			for (String getter: columns.getGetters())
			{
				List<VCardParameter> types = null;
				String value = _getCardValue(property, getter, name);
				if (columns.getTyped())
				{
					types = (List<VCardParameter>) property.getClass().getMethod("getTypes").invoke(property);
				}
				database.parseCard(id, columns.getColumnId(types, getter), value);
			}
		}
	};

	private String _getCardValue(T property,
								 String getter,
								 String name)
	throws IllegalAccessException, 
	IllegalArgumentException, 
	InvocationTargetException,
	NoSuchMethodException,
	SecurityException
	{
		String value = null;
		Method method = property.getClass().getMethod(getter);
		Class<?> clazz = method.getReturnType();
		System.out.println("CardProperty._getCardValue(): 1 Name: " + name + " - Class: " + clazz.getName());
		if (clazz.getName().equals("java.util.List"))
		{
			//List<String> list = Stream.of(object).map(Object::toString).collect(Collectors.toList());
			@SuppressWarnings("unchecked")
			List<String> list = (List<String>) method.invoke(property);
			if (list.size() > 0)
			{
				value = list.get(0);
				System.out.println("CardProperty._getCardValue(): 2 Name: " + name + " - List: " + list + " - Size: " + list.size() + " - Value: " + value);
			}
		}
		else value = (String) method.invoke(property);
		return value;
	}
	
}
