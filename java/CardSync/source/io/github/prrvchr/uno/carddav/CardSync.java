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


import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.sql.Timestamp;
import java.util.List;
import java.util.Map;

import com.github.mangstadt.vinnie.VObjectProperty;
import com.github.mangstadt.vinnie.io.Context;
import com.github.mangstadt.vinnie.io.SyntaxRules;
import com.github.mangstadt.vinnie.io.VObjectDataAdapter;
import com.github.mangstadt.vinnie.io.VObjectReader;

import com.sun.star.beans.NamedValue;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.Type;
import com.sun.star.uno.XComponentContext;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.sdbc.XConnection;
import com.sun.star.task.XJob;
import com.sun.star.util.DateTime;

import io.github.prrvchr.uno.lang.ServiceComponent;
import io.github.prrvchr.uno.helper.UnoHelper;


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
		m_xContext = context;
	};

	// com.sun.star.lang.XServiceInfo:
	@Override
	public String _getImplementationName()
	{
		return m_name;
	}

	@Override
	public String[] _getServiceNames()
	{
		return m_services;
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
	{
		System.out.println("CardSync.execute() 1");
		DataBase database = new DataBase(_getConnection(arguments));
		try
		{
			System.out.println("CardSync.execute() 2");
			String name = database.getUserName();
			System.out.println("CardSync.execute() 3");
			String version = database.getDriverVersion();
			System.out.println("CardSync.execute() 4 Name: " + name + " - Version: " + version);
			long ts = System.currentTimeMillis();
			DateTime first = UnoHelper.getUnoDateTime(new DateTime(), new Timestamp(ts));
			//DateTime last = UnoHelper.getUnoDateTime(new DateTime(), new Timestamp(ts));;
			List<Map<String, Object>> cards = database.getChangedCards(first);
			System.out.println("CardSync.execute() 5");
			int i = cards.size();
			System.out.println("CardSync.execute() 6");
			for (int j = 0; j < i; j++)
			{
				System.out.println("CardSync.execute() 7");
				_syncCard(database, cards.get(j));
				System.out.println("CardSync.execute() 8");
			}
			System.out.println("CardSync.execute() 9");
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("CardSync.execute() 12");
		return null;
	}

	private XConnection _getConnection(NamedValue[] arguments)
	{
		XConnection connection = null;
		int i = arguments.length;
		for (int j = 0; j < i; j++)
		{
			if (arguments[j].Name.equals("DynamicData"))
			{
				NamedValue[] data = (NamedValue[]) AnyConverter.toArray(arguments[j].Value);
				int k = data.length;
				for (int l = 0; l < k; l++)
				{
					if (data[l].Name.equals("Connection"))
					{
						connection = (XConnection) AnyConverter.toObject(new Type(XConnection.class), data[l].Value);
						break;
					}
				}
				break;
			}
		}
		return connection;
	}

	private void _syncCard(DataBase database, Map<String, Object> card) throws IOException
	{
		int deleted = 0;
		int updated = 0;
		int inserted = 0;
		int id = (int) card.get("Card");
		String data = (String) card.get("Data");
		String method = (String) card.get("Method");
		DateTime order = (DateTime) card.get("Order");
		if (method.equals("Deleted"))
		{
			System.out.println("CardSync._syncCard() Delete");
			deleted += database.deleteCard(id);
		}
		else
		{
			_parseCard(id, method, data);
		}
	}

	private void _parseCard(int id, String method, String data) throws IOException
	{
		
		Reader reader = new StringReader(data);
		SyntaxRules rules = SyntaxRules.vcard();
		VObjectReader vobjectReader = new VObjectReader(reader, rules);
		vobjectReader.parse(new VObjectDataAdapter()
		{
			private boolean inVCard = false;

			public void onComponentBegin(String name, Context context)
			{
				if (context.getParentComponents().isEmpty() && "VCARD".equals(name))
				{
					inVCard = true;
				}
			}

			public void onComponentEnd(String name, Context context)
			{
				if (context.getParentComponents().isEmpty())
				{
					//end of vCard, stop parsing
					context.stop();
				}
			}

			public void onProperty(VObjectProperty property, Context context)
			{
				if (inVCard)
				{
					System.out.println(property.getName() + " = " + property.getValue());
				}
			}
		});
		vobjectReader.close();
	
	}


}
