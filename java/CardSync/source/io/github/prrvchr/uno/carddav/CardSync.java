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
import java.sql.Timestamp;
import java.util.Map;

import ezvcard.Ezvcard;
import ezvcard.VCard;
import ezvcard.io.scribe.ScribeIndex;
import ezvcard.property.Address;
import ezvcard.property.Categories;
import ezvcard.property.Email;
import ezvcard.property.Telephone;
import ezvcard.property.Title;
import ezvcard.property.VCardProperty;

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
		DataBase database = new DataBase(arguments);
		try
		{
			System.out.println("CardSync.execute() 2");
			String name = database.getUserName();
			System.out.println("CardSync.execute() 3");
			String version = database.getDriverVersion();
			System.out.println("CardSync.execute() 4 Name: " + name + " - Version: " + version);
			long ts = System.currentTimeMillis();
			DateTime first = UnoHelper.getUnoDateTime(new DateTime(), new Timestamp(ts - 100000000));
			DateTime last = UnoHelper.getUnoDateTime(new DateTime(), new Timestamp(ts));
			System.out.println("CardSync.execute() 5");
			for (Map<String, Object> card: database.getChangedCards(first, last))
			{
				int id = (int) card.get("Card");
				String method = (String) card.get("Method");
				String data = (String) card.get("Data");
				_syncCard(database, id, method, data);
			}
			System.out.println("CardSync.execute() 6");
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("CardSync.execute() 7");
		return null;
	}

	private void _syncCard(DataBase database, int id, String method, String data) throws IOException
	{
		@SuppressWarnings("unused")
		int deleted = 0;
		@SuppressWarnings("unused")
		int updated = 0;
		@SuppressWarnings("unused")
		int inserted = 0;
		if (!method.equals("Deleted"))
		{
			_parseCard(id, method, data);
		}
	}

	private void _parseCard(int id, String method, String data) throws IOException
	{
		VCard card = Ezvcard.parse(data).first();
		ScribeIndex index = new ScribeIndex();
		for (VCardProperty property: card)
		{
			String name = index.getPropertyScribe(property).getPropertyName();
			if ("FN".equals(name)) _parseFormattedName(card, id, method);
			else if ("ADR".equals(name)) _parseAddresses(card, id, method);
			else if ("EMAIL".equals(name)) _parseEmails(card, id, method);
			else if ("TEL".equals(name)) _parseTelephones(card, id, method);
			else if ("TITLE".equals(name)) _parseTitles(card, id, method);
			else if ("CATEGORIES".equals(name)) _parseCategories(card, id, method);
			else System.out.println("CardSync._parseCard() " + name);
		}
	}

	private void _parseFormattedName(VCard card, int id, String method)
	{

		String name = card.getFormattedName().getValue();
		System.out.println("CardSync._parseFormattedName() '" + name + "'");
	}

	private void _parseAddresses(VCard card, int id, String method)
	{
		for (Address address: card.getAddresses())
		{
			String street = address.getStreetAddress();
			String city = address.getLocality();
			System.out.println("CardSync._parseAddresses() Street: " + street + " - City: " + city);
		}
	}

	private void _parseEmails(VCard card, int id, String method)
	{
		for (Email email: card.getEmails())
		{
			String value = email.getValue();
			System.out.println("CardSync._parseEmails() " + value);
		}
	}

	private void _parseTelephones(VCard card, int id, String method)
	{
		for (Telephone telephone: card.getTelephoneNumbers())
		{
			String value = telephone.getText();
			System.out.println("CardSync._parseTelephones() " + value);
		}
	}

	private void _parseTitles(VCard card, int id, String method)
	{
		for (Title title: card.getTitles())
		{
			String value = title.getValue();
			System.out.println("CardSync._parseTitles() " + value);
		}
	}

	private void _parseCategories(VCard card, int id, String method)
	{
		for (Categories categories: card.getCategoriesList())
		{
			for (String category: categories.getValues())
			{
				System.out.println("CardSync._parseCategories() " + category);
			}
		}
	}

}
