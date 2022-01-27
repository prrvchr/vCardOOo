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
package io.github.prrvchr.carddav;


import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;

import ezvcard.Ezvcard;
import ezvcard.VCard;
import ezvcard.io.scribe.ScribeIndex;
import ezvcard.property.VCardProperty;

import com.sun.star.beans.NamedValue;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.uno.XComponentContext;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.sdbc.SQLException;
import com.sun.star.task.XJob;

import io.github.prrvchr.uno.lang.ServiceComponent;


public final class CardSync
extends ServiceComponent
implements XJob
{
	@SuppressWarnings("unused")
	private final XComponentContext m_xContext;
	private static final String m_name = CardSync.class.getName();
	private static final String[] m_services = {"io.github.prrvchr.vCardOOo.CardSync",
                                                "com.sun.star.task.Job"};
	@SuppressWarnings("unused")
	private static final String m_identifier = "io.github.prrvchr.vCardOOo";

	public CardSync(XComponentContext context)
	{
		super(m_name, m_services);
		m_xContext = context;
	}


	// UNO Service Registration:
	public static XSingleComponentFactory __getComponentFactory(String name)
	{
		XSingleComponentFactory xFactory = null;
		if (name.equals(m_name))
		{
			xFactory = Factory.createComponentFactory(CardSync.class, m_services);
		}
		return xFactory;
	}

	public static boolean __writeRegistryServiceInfo(XRegistryKey key)
	{
		return Factory.writeRegistryServiceInfo(m_name, m_services, key);
	}

	// com.sun.star.task.XJob:
	public Object execute(NamedValue[] arguments)
	throws SQLException
	{
		DataBase database = new DataBase(arguments);
		Map<Integer, CardGroup> groups = database.getCardGroup();
		try
		{
			boolean status = true;
			String name = database.getUserName();
			String version = database.getDriverVersion();
			System.out.println("CardSync.execute() 1 Name: " + name + " - Version: " + version);
			Map<String, CardColumn> columns = database.getAddressbookColumn();
			//for (String key: columns.keySet())
			//{
			//	CardColumn column = columns.get(key);
			//	for (Map<String, Object> object: column.getColumns())
			//	{
			//		System.out.println("CardSync.execute() 2 Key: " + key + " - Map: " + object);
			//	}
			//}
			for (Map<String, Object> result: database.getChangedCards())
			{
				System.out.println("CardSync.execute() 3");
				String query = (String) result.get("Query");
				if (!query.equals("Deleted"))
				{
					System.out.println("CardSync.execute() 4");
					int user = (int) result.get("User");
					int card = (int) result.get("Card");
					String data = (String) result.get("Data");
					status = _parseCard(database, groups.get(user), card, data, columns);
				}
			}
			if (status) database.updateUser();
			System.out.println("CardSync.execute() 5");
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("CardSync.execute() 3");
		return null;
	}

	private boolean _parseCard(DataBase database,
							   CardGroup group,
							   int id,
							   String data,
							   Map<String, CardColumn> columns)
	throws IOException,
		   NoSuchMethodException,
		   IllegalAccessException,
		   IllegalArgumentException,
		   InvocationTargetException,
		   SecurityException,
		   SQLException,
		   InstantiationException
	{
		VCard card = Ezvcard.parse(data).first();
		ScribeIndex index = new ScribeIndex();
		int i = 0;
		for (VCardProperty property: card)
		{
			String name = index.getPropertyScribe(property).getPropertyName();
			// XXX: We do not parse Properties that do not have a Column
			if (!columns.containsKey(name))
			{
				continue;
			}
			System.out.println("CardSync.parseCard(): 1 Property" + name + " - Num: " + i);
			CardColumn column = columns.get(name);
			_parseCardProperty(database, group, id, card, column);
			i ++;
		}
		return true;
	}

	private <T> void _parseCardProperty(DataBase database,
										CardGroup group,
										int id,
										VCard card,
										CardColumn column)
	throws NoSuchMethodException,
		   IllegalAccessException,
		   IllegalArgumentException,
		   InvocationTargetException,
		   SecurityException,
		   SQLException,
		   InstantiationException
	{
		CardProperty<T> property = new CardProperty<T>(card, column);
		property.parse(database, group, id, column);
	}


}
