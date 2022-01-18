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
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Objects;

import com.sun.star.sdbc.SQLException;

import ezvcard.VCard;
import ezvcard.parameter.VCardParameter;


public final class CardProperty<T>
{

	private List<T> m_properties = null;

	// FIXME: Suppress Warnings unchecked
	@SuppressWarnings("unchecked")
	public CardProperty(VCard card,
						CardColumn column)
	throws NoSuchMethodException,
		   SecurityException,
		   IllegalAccessException,
		   IllegalArgumentException,
		   InvocationTargetException
	{
		Object object = card.getClass().getDeclaredMethod(column.getMethod()).invoke(card);
		if (object instanceof List)
		{
			m_properties = (List<T>) object;
			
		}
		else
		{
			m_properties = new ArrayList<T>(Arrays.asList((T) object));
		}
	}

	// FIXME: Suppress Warnings unchecked
	@SuppressWarnings("unchecked")
	public void parse(DataBase database,
					  CardGroup group,
					  int card,
					  CardColumn columns)
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
				if (columns.isGroup())
				{
					group.parse(database, card, _getCardGroup(property, getter));
				}
				else
				{
					List<VCardParameter> types = null;
					String value = _getCardValue(property, getter);
					if (columns.isTyped())
					{
						types = (List<VCardParameter>) property.getClass().getMethod("getTypes").invoke(property);
					}
					Integer column = columns.getColumnId(types, getter);
					if (column != null)
					{
						database.parseCard(card, column, value);
					}
				}
			}
		}
	}

	private String[] _getCardGroup(T property,
								   String getter)
	throws IllegalAccessException,
		   IllegalArgumentException,
		   InvocationTargetException,
		   NoSuchMethodException,
		   SecurityException
	{
		Object object = property.getClass().getMethod(getter).invoke(property);
		List<?> list = _convertObjectToList(object);
		List<String> strings = new ArrayList<>(list.size());
		for (Object o: list)
		{
			strings.add(Objects.toString(o, null));
		}
		System.out.println("CardProperty._getCardGroup(): 1 List: " + strings);
		return strings.toArray(new String[0]);
	}

	private String _getCardValue(T property,
								 String getter)
	throws IllegalAccessException,
		   IllegalArgumentException,
		   InvocationTargetException,
		   NoSuchMethodException,
		   SecurityException
	{
		String value = null;
		Object object = property.getClass().getMethod(getter).invoke(property);
		if (object instanceof List)
		{
			List<?> list = (List<?>) object;
			if (list.size() > 0)
			{
				value = (String) list.get(0);
			}
		}
		else
		{
			value = (String) object;
		}
		System.out.println("CardProperty._getCardValue(): 1 Value: " + value);
		return value;
	}

	private List<?> _convertObjectToList(Object object)
	{
		List<?> list = new ArrayList<>();
		if (object.getClass().isArray())
		{
			list = Arrays.asList((Object[]) object);
		}
		else if (object instanceof Collection)
		{
			list = new ArrayList<>((Collection<?>) object);
		}
		System.out.println("CardProperty._convertObjectToList(): 1 List: " + list);
		return list;
	}


}
