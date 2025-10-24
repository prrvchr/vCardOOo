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

import java.util.HashMap;
import java.util.Map;

import org.json.JSONObject;

import com.sun.star.sdbc.SQLException;


public final class Organizer {

    private Map<String, CardProperty> mProperties = new HashMap<>();
    private Map<Integer, JSONObject> mGroups = new HashMap<>();

    public Organizer(DataBase database)
        throws SQLException {
        mProperties = database.getCardProperties();
        mGroups = database.getCardGroup();
    }

    public boolean supportProperty(String name) {
        return mProperties.containsKey(name);
    }

    public boolean supportField(String name) {
        return true;
    }

    public CardProperty getProperty(String name) {
        return mProperties.get(name);
    }

    public boolean isGroupProperty(String name) {
        return mProperties.containsKey(name) & mProperties.get(name).isGroup();
    }

    public boolean isTypedProperty(String name) {
        return mProperties.containsKey(name) & mProperties.get(name).isTyped();
    }

    public boolean hasGroup(Integer user, String name) {
        boolean has = false;
        if (mGroups.containsKey(user)) {
            has = mGroups.get(user).has(name);
        }
        return has;
    }

    public Integer getGroupId(Integer user, String name) {
        Integer groupid = -1;
        if (mGroups.containsKey(user) & mGroups.get(user).has(name)) {
            groupid = mGroups.get(user).getInt(name);
        }
        return groupid;
    }

}
