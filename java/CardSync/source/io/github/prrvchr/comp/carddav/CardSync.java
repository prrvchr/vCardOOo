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
package io.github.prrvchr.comp.carddav;

import com.sun.star.beans.NamedValue;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.uno.XComponentContext;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.task.XJob;

import io.github.prrvchr.comp.lang.ServiceComponent;

public final class CardSync
extends ServiceComponent
implements XJob
{
	private final XComponentContext m_xContext;
	private static final String m_name = CardSync.class.getName();
	private static final String[] m_services = {"io.github.prrvchr.vCardOOo.CardSync",
                                                "com.sun.star.task.Job"};
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
		if ( name.equals(m_name))
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
	public Object execute(NamedValue[] values)
	{
		System.out.println("CardSync.execute() 1");
		int len = values.length;
		for (int i = 0; i < len; i++)
		{
			NamedValue value = values[i];
			System.out.println("CardSync.execute() 2 Name: " + value.Name + " - Value: " + value.Value.toString());
		}
		System.out.println("CardSync.execute() 3");
		return null;
	}


}
