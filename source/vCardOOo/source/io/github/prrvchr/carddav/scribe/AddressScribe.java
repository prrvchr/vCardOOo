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
package io.github.prrvchr.carddav.scribe;

import com.github.mangstadt.vinnie.io.VObjectPropertyValues.SemiStructuredValueBuilder;
import com.github.mangstadt.vinnie.io.VObjectPropertyValues.SemiStructuredValueIterator;
import com.github.mangstadt.vinnie.io.VObjectPropertyValues.StructuredValueBuilder;
import com.github.mangstadt.vinnie.io.VObjectPropertyValues.StructuredValueIterator;

import ezvcard.VCardDataType;
import ezvcard.VCardVersion;
import ezvcard.io.ParseContext;
import ezvcard.io.scribe.VCardPropertyScribe;
import ezvcard.io.text.WriteContext;
import ezvcard.parameter.VCardParameters;
import static ezvcard.util.StringUtils.join;
import io.github.prrvchr.carddav.property.Address;


public final class AddressScribe extends VCardPropertyScribe<Address>
{
    public AddressScribe() {
        super(Address.class, "ADR");
    }

    @Override
    protected VCardDataType _defaultDataType(VCardVersion version) {
        return VCardDataType.TEXT;
    }

    @Override
    protected Address _parseText(String value, VCardDataType dataType, VCardParameters parameters, ParseContext context) {
        if (context.getVersion() == VCardVersion.V2_1) {
            /*
             * 2.1 does not recognize multi-valued components.
             */
            SemiStructuredValueIterator it = new SemiStructuredValueIterator(value);
            return parseSemiStructuredValue(it);
        } else {
            StructuredValueIterator it = new StructuredValueIterator(value);
            return parseStructuredValue(it);
        }
    }

    @Override
    protected String _writeText(Address property, WriteContext context) {
        /*
         * StructuredValueBuilder cannot be used with 2.1 because it escapes
         * comma characters. For example, if someone's street address is
         * "Foo,bar Lane", the comma character must NOT be escaped when written
         * to a 2.1 vCard.
         * 
         * The reason commas are not escaped in 2.1 is because 2.1 does not
         * allow multi-valued components like 3.0 and 4.0 do (for example,
         * multiple street addresses).
         * 
         * If an Address object has multi-valued components, and it is being
         * written to a 2.1 vCard, then ez-vcard will comma-delimit them to
         * prevent data loss. But this is not part of the 2.1 syntax.
         */
        if (context.getVersion() == VCardVersion.V2_1) {
            SemiStructuredValueBuilder builder = new SemiStructuredValueBuilder();
            builder.append(join(property.getPoBoxes(), ","));
            builder.append(join(property.getExtendedAddresses(), ","));
            builder.append(join(property.getStreetAddresses(), ","));
            builder.append(join(property.getLocalities(), ","));
            builder.append(join(property.getRegions(), ","));
            builder.append(join(property.getPostalCodes(), ","));
            builder.append(join(property.getCountries(), ","));
            return builder.build(false, context.isIncludeTrailingSemicolons());
        } else {
            StructuredValueBuilder builder = new StructuredValueBuilder();
            builder.append(property.getPoBoxes());
            builder.append(property.getExtendedAddresses());
            builder.append(property.getStreetAddresses());
            builder.append(property.getLocalities());
            builder.append(property.getRegions());
            builder.append(property.getPostalCodes());
            builder.append(property.getCountries());
            return builder.build(context.isIncludeTrailingSemicolons());
        }
    }

    private static Address parseStructuredValue(StructuredValueIterator it) {
        Address property = new Address();

        property.getPoBoxes().addAll(it.nextComponent());
        property.getExtendedAddresses().addAll(it.nextComponent());
        property.getStreetAddresses().addAll(it.nextComponent());
        property.getLocalities().addAll(it.nextComponent());
        property.getRegions().addAll(it.nextComponent());
        property.getPostalCodes().addAll(it.nextComponent());
        property.getCountries().addAll(it.nextComponent());

        return property;
    }

    private static Address parseSemiStructuredValue(SemiStructuredValueIterator it) {
        Address property = new Address();

        String next = it.next();
        if (next != null) {
            property.getPoBoxes().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getExtendedAddresses().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getStreetAddresses().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getLocalities().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getRegions().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getPostalCodes().add(next);
        }

        next = it.next();
        if (next != null) {
            property.getCountries().add(next);
        }

        return property;
    }


}

