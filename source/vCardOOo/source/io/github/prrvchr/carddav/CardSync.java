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

import com.sun.star.lang.XServiceInfo;

import java.util.Map.Entry;

import com.sun.star.beans.NamedValue;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.util.DateTimeWithTimezone;

import com.sun.star.sdbc.SQLException;
import com.sun.star.sdbc.XPreparedStatement;
import com.sun.star.sdbc.XResultSet;
import com.sun.star.sdbc.XRow;
import com.sun.star.task.XJob;

import io.github.prrvchr.uno.helper.UnoHelper;
import io.github.prrvchr.uno.helper.ServiceInfo;
import io.github.prrvchr.carddav.scribe.FormattedNameScribe;
import io.github.prrvchr.carddav.scribe.OrganizationScribe;
import io.github.prrvchr.carddav.scribe.StructuredNameScribe;
import io.github.prrvchr.carddav.scribe.TelephoneScribe;
import io.github.prrvchr.carddav.scribe.TitleScribe;
import io.github.prrvchr.carddav.scribe.UidScribe;
import io.github.prrvchr.carddav.scribe.AddressScribe;
import io.github.prrvchr.carddav.scribe.CategoriesScribe;
import io.github.prrvchr.carddav.scribe.EmailScribe;

import com.sun.star.lib.uno.helper.ComponentBase;

import ezvcard.VCard;
import ezvcard.io.scribe.ScribeIndex;
import ezvcard.io.text.VCardReader;
import ezvcard.property.VCardProperty;


public final class CardSync
    extends ComponentBase
    implements XServiceInfo,
               XJob {

    private static final String mImplementationName = CardSync.class.getName();
    private static final String[] m_serviceNames = {"io.github.prrvchr.vCardOOo.CardSync",
                                                    "com.sun.star.task.Job"};
    @SuppressWarnings("unused")
    private static final String m_identifier = "io.github.prrvchr.vCardOOo";
    @SuppressWarnings("unused")
    private XComponentContext mContext;

    public CardSync(XComponentContext context) {
        super();
        mContext = context;
    }

    // com.sun.star.lang.XServiceInfo:
    @Override
    public String getImplementationName() {
        return ServiceInfo.getImplementationName(mImplementationName);
    }

    @Override
    public String[] getSupportedServiceNames() {
        return ServiceInfo.getSupportedServiceNames(m_serviceNames);
    }

    @Override
    public boolean supportsService(String service) {
        return ServiceInfo.supportsService(m_serviceNames, service);
    }


    // com.sun.star.task.XJob:
    public Object execute(NamedValue[] arguments)
        throws SQLException {
        int cnum = 0;
        int gnum = 0;
        DataBase database = new DataBase(arguments);
        if (database.prepareBatchCall()) {
            Organizer organizer = new Organizer(database);
            DateTimeWithTimezone start = database.getLastUserSync();
            DateTimeWithTimezone stop = UnoHelper.currentDateTimeInTZ();
            XPreparedStatement call = database.getChangedCards(start, stop);
            XResultSet result = call.executeQuery();
            XRow row = UnoRuntime.queryInterface(XRow.class, result);
            ScribeIndex index = new ScribeIndex();
            index.register(new UidScribe());
            index.register(new FormattedNameScribe());
            index.register(new EmailScribe());
            index.register(new AddressScribe());
            index.register(new StructuredNameScribe());
            index.register(new OrganizationScribe());
            index.register(new TelephoneScribe());
            index.register(new TitleScribe());
            index.register(new CategoriesScribe());
            final int UID = 1;
            final int CID = 2;
            final int STATE = 3;
            final int VALUE = 4;
            try {
                while (result != null && result.next()) {
                    int uid = row.getInt(UID);
                    int cid = row.getInt(CID);
                    if (!row.getString(STATE).equals("Deleted")) {
                        VCardReader reader = new VCardReader(row.getString(VALUE));
                        reader.setScribeIndex(index);
                        VCard vcard = reader.readNext();
                        reader.close();
                        for (VCardProperty property : vcard.getProperties()) {
                            String prefix = index.getPropertyScribe(property).getPropertyName();
                            if (! organizer.supportProperty(prefix)) {
                                continue;
                            }
                            if (organizer.isGroupProperty(prefix)) {
                                gnum += mergeGroup(database, organizer, property, uid, cid);
                            } else {
                                cnum += mergeCardData(database, organizer, property, cid, prefix);
                            }
                        }
                    }
                }
                database.commitBatchCall(cnum, gnum, stop);
                database.close(result);
                database.close(call);
            } catch (Exception e) {
                System.out.println("Error happened: " + e.getMessage());
                e.printStackTrace();
            }
        }
        return null;
    }

    private int mergeGroup(DataBase database, Organizer organizer,
                           VCardProperty property, int uid, int cid)
        throws SQLException {
        int gnum = 0;
        for (String group : property.getPropertyCategories()) {
            if (organizer.hasGroup(uid, group)) {
                gnum += database.mergeGroup(cid, organizer.getGroupId(uid, group));
            }
        }
        return gnum;
    }

    private int mergeCardData(DataBase database, Organizer organizer,
                              VCardProperty property, int cid, String prefix)
        throws SQLException {
        int cnum = 0;
        for (Entry<String, String> entry : property.getPropertiesValue().entrySet()) {
            String field = entry.getKey();
            String data = entry.getValue();
            // XXX: We must parse only the property that we have
            // XXX: previously configured in the database
            if (organizer.supportField(field)) {
                // XXX: If the property is typed, then we need to get its type
                // XXX: so we can find the column, from the database table,
                // XXX: into which the value will be inserted
                String[] suffixes = new String[0];
                if (organizer.isTypedProperty(prefix)) {
                    suffixes = property.getPropertyTypes();
                }
                cnum += database.mergeCardData(cid, prefix, field, suffixes, data);
            }
        }
        return cnum;
    }

}
