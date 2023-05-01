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
package io.github.prrvchr.carddav.property;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import ezvcard.parameter.AddressType;


public class Address extends ezvcard.property.Address
{
    public Address() {
          super();
    }
    public Address(Address original) {
        super(original);
    }

    @Override
    public int hashCode() {
        return super.hashCode();
    }
    @Override
    public boolean equals(Object obj) {
        return super.equals(obj);
    }

    public Map<String, String> getPropertiesValue() {
        Map<String, String> values = new LinkedHashMap<>();
        if (getPoBox() != null) values.put("poBox", getPoBox());
        if (getExtendedAddress() != null) values.put("extendedAddress", getExtendedAddress());
        if (getStreetAddress() != null) values.put("streetAddress", getStreetAddress());
        if (getLocality() != null) values.put("locality", getLocality());
        if (getRegion() != null) values.put("region", getRegion());
        if (getPostalCode() != null) values.put("postalCode", getPostalCode());
        if (getCountry() != null) values.put("country", getCountry());
        return values;
    }

    public String[] getPropertyTypes() {
        List<String> types = new ArrayList<String>();
        for (AddressType type : getTypes()) {
            types.add(type.getValue());
        }
        return types.toArray(new String[0]);
    }

}

