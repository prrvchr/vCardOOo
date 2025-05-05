/*
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020-25 https://prrvchr.github.io                                  ║
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

import org.json.JSONObject;


public final class CardProperty
{

    private final String m_name;
    private final String m_getter;
    private final boolean m_isgroup;
    private final boolean m_istyped;
    private final JSONObject m_methods;

    public CardProperty(String name,
                        String getter,
                        boolean isgroup,
                        boolean istyped,
                        JSONObject methods)
    {
        m_name = name;
        m_getter = getter;
        m_isgroup = isgroup;
        m_istyped = istyped;
        m_methods = methods;
    }

    public String getName()
    {
        return m_name;
    }

    public String getGetter()
    {
        return m_getter;
    }

    public Boolean isGroup()
    {
        if (m_isgroup) {
            System.out.println("CardProperty.isGroup() IsGroup: " + m_isgroup);
        }
        return m_isgroup;
    }

    public Boolean isTyped()
    {
        return m_istyped;
    }

    public String[] getMethods()
    {
        return (String[]) m_methods.keySet().toArray();
    }

    public String getLabel(String name)
    {
        if (m_methods.has(name)) {
            return m_methods.getString(name);
        }
        return null;
    }

}
