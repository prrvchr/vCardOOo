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
package io.github.prrvchr.carddav.scribe;


import java.util.List;

import com.github.mangstadt.vinnie.io.VObjectPropertyValues;

import ezvcard.VCardDataType;
import ezvcard.VCardVersion;
import ezvcard.io.ParseContext;
import ezvcard.io.scribe.VCardPropertyScribe;
import ezvcard.io.text.WriteContext;
import ezvcard.parameter.VCardParameters;
import io.github.prrvchr.carddav.property.Organization;


public final class OrganizationScribe extends VCardPropertyScribe<Organization>
{
    public OrganizationScribe() {
        super(Organization.class, "ORG");
    }

    @Override
    protected VCardDataType _defaultDataType(VCardVersion version) {
        return VCardDataType.TEXT;
    }

    @Override
    protected String _writeText(Organization property, WriteContext context) {
        boolean escapeCommas = (context.getVersion() != VCardVersion.V2_1);
        return VObjectPropertyValues.writeSemiStructured(property.getValues(), escapeCommas, context.isIncludeTrailingSemicolons());
    }

    @Override
    protected Organization _parseText(String value, VCardDataType dataType, VCardParameters parameters, ParseContext context) {
        Organization property = new Organization();

        List<String> values = VObjectPropertyValues.parseSemiStructured(value);
        property.getValues().addAll(values);

        return property;
    }

}
