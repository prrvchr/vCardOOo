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
import java.util.Map;

import ezvcard.VCard;


public final class CardProperty
{

	private Object m_property = null;

	public CardProperty(DataBase database,
						VCard card,
						Map<String, Object> result,
						CardColumn column,
						String query)
	throws NoSuchMethodException, IllegalAccessException, IllegalArgumentException, InvocationTargetException
	{
		String name = column.getMethod();
		System.out.println("CardProperty.CardProperty()1 " + name);
		//Method method = card.getClass().getDeclaredMethod(name);
		//Class<?> cls = method.getReturnType();
		//m_property = method.invoke(card);
		//System.out.println("CardProperty.CardProperty()2 " + cls.getName() + " - " + m_property.getClass().getName() + " - " + clazz.getName());
	};


}
