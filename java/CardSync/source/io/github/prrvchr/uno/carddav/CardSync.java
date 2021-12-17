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
import java.util.Map;

import ezvcard.Ezvcard;
import ezvcard.VCard;
import ezvcard.io.scribe.ScribeIndex;
import ezvcard.parameter.EmailType;
import ezvcard.parameter.TelephoneType;
import ezvcard.property.Address;
import ezvcard.property.Categories;
import ezvcard.property.Email;
import ezvcard.property.FormattedName;
import ezvcard.property.Organization;
import ezvcard.property.StructuredName;
import ezvcard.property.Telephone;
import ezvcard.property.Title;
import ezvcard.property.VCardProperty;

import com.sun.star.beans.NamedValue;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.uno.XComponentContext;
import com.sun.star.registry.XRegistryKey;
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
		DataBase database = new DataBase(arguments);
		try
		{
			String name = database.getUserName();
			String version = database.getDriverVersion();
			System.out.println("CardSync.execute() 1 Name: " + name + " - Version: " + version);
			for (Map<String, Object> result: database.getChangedCards())
			{
				String method = (String) result.get("Method");
				if (!method.equals("Deleted")) _parseCard(database, result, method);
			}
			database.setTimestamp();
			System.out.println("CardSync.execute() 2");
		}
		catch (Exception e)
		{
			System.out.println("Error happened: " + e.getMessage());
			e.printStackTrace();
		}
		System.out.println("CardSync.execute() 3");
		return null;
	}

	private void _parseCard(DataBase database, Map<String, Object> result, String method) throws IOException
	{
		String data = (String) result.get("Data");
		VCard card = Ezvcard.parse(data).first();
		ScribeIndex index = new ScribeIndex();
		for (VCardProperty property: card)
		{
			String name = index.getPropertyScribe(property).getPropertyName();
			if ("FN".equals(name)) _parseFormattedNames(card, result, method);
			else if ("N".equals(name)) _parseStructuredNames(card, result, method);
			else if ("EMAIL".equals(name)) _parseEmails(card, result, method);
			else if ("ORG".equals(name)) _parseOrganizations(card, result, method);
			else if ("ADR".equals(name)) _parseAddresses(card, result, method);
			else if ("TEL".equals(name)) _parseTelephones(card, result, method);
			else if ("TITLE".equals(name)) _parseTitles(card, result, method);
			else if ("CATEGORIES".equals(name)) _parseCategories(database, card, result, method);
			else System.out.println("CardSync._parseCard() " + name);
		}
	}

	private void _parseFormattedNames(VCard card, Map<String, Object> result, String method)
	{
		for (FormattedName name: card.getFormattedNames())
		{
			
			String fullname = name.getValue();
			System.out.println("CardSync._parseFormattedNames() '" + fullname + "'");
		}
	}

	private void _parseStructuredNames(VCard card, Map<String, Object> result, String method)
	{
		for (StructuredName name: card.getStructuredNames())
		{
			String firstname = name.getGiven();
			String lastname = name.getFamily();
			System.out.println("CardSync._parseStructuredNames() Fisrt Name: " + firstname + " - Last Name: " + lastname);
		}
	}

	private void _parseEmails(VCard card, Map<String, Object> result, String method)
	{
		for (Email email: card.getEmails())
		{
			String value = email.getValue();
			for (EmailType type: email.getTypes())
			{
				System.out.println("CardSync._parseEmails() N°: " + value + " - Type: " + type.getValue());
			}
		}
	}

	private void _parseOrganizations(VCard card, Map<String, Object> result, String method)
	{
		for (Organization organization: card.getOrganizations())
		{
			for (String value: organization.getValues())
			{
				System.out.println("CardSync._parseOrganizations() " + value);
			}
		}
	}

	private void _parseAddresses(VCard card, Map<String, Object> result, String method)
	{
		for (Address address: card.getAddresses())
		{
			String street = address.getStreetAddress();
			String city = address.getLocality();
			System.out.println("CardSync._parseAddresses() Street: " + street + " - City: " + city);
		}
	}

	private void _parseTelephones(VCard card, Map<String, Object> result, String method)
	{
		for (Telephone telephone: card.getTelephoneNumbers())
		{
			String value = telephone.getText();
			for (TelephoneType type: telephone.getTypes())
			{
				System.out.println("CardSync._parseTelephones() N°: " + value + " - Type: " + type.getValue());
			}
		}
	}

	private void _parseTitles(VCard card, Map<String, Object> result, String method)
	{
		for (Title title: card.getTitles())
		{
			String value = title.getValue();
			System.out.println("CardSync._parseTitles() " + value);
		}
	}

	private void _parseCategories(DataBase database, VCard card, Map<String, Object> result, String method)
	{
		for (Categories categories: card.getCategoriesList())
		{
			for (String category: categories.getValues())
			{
				//database.updateGroup(category, card);
				int user = (int) result.get("User");
				System.out.println("CardSync._parseCategories() User: " + user + " - Group: " + category);
			}
		}
	}


}
