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


import java.util.HashMap;
import java.util.Map;

import com.sun.star.sdbc.SQLException;

import io.github.prrvchr.uno.helper.Array;


public final class CardGroup
{

    private Integer m_user = null;
    private Map<String, Integer> m_groups = null;

    public CardGroup(Map<String, Object> map,
                    String key,
                    String name,
                    String group)
    throws SQLException
    {
        m_user = (Integer) map.get(key);
        Map<String, Integer> maps = new HashMap<String, Integer>();
        Object[] names = ((Array) map.get(name)).getArray(null);
        Object[] groups = ((Array) map.get(group)).getArray(null);
        for (int i=0; i<names.length; i++) {
            maps.put((String) names[i], (Integer) groups[i]);
        }
        m_groups = maps;
    }

    
    public void parse(DataBase database,
                      int card,
                      String[] groups)
    throws SQLException
    {
        for (int i=0; i<groups.length; i++) {
            String group = groups[i];
            if (!m_groups.containsKey(group)) {
                m_groups.put(group, database.insertGroup(m_user, group));
            }
        }
        database.mergeGroup(card, _getGroupIds(groups));
    }

    public Integer getUser()
    {
        return m_user;
    }

    private Object[] _getGroupIds(String[] groups)
    {
        Object[] ids = new Object[groups.length];
        for (int i=0; i<groups.length; i++) {
            ids[i] = m_groups.get(groups[i]);
            
        }
        return ids;
    }
}
