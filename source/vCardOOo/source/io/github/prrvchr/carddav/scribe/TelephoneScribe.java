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


import com.github.mangstadt.vinnie.io.VObjectPropertyValues;

import ezvcard.VCardDataType;
import ezvcard.VCardVersion;
import ezvcard.io.ParseContext;
import ezvcard.io.scribe.VCardPropertyScribe;
import ezvcard.io.text.WriteContext;
import ezvcard.parameter.VCardParameters;
import ezvcard.util.TelUri;
import io.github.prrvchr.carddav.property.Telephone;


public final class TelephoneScribe extends VCardPropertyScribe<Telephone> {
    public TelephoneScribe() {
        super(Telephone.class, "TEL");
    }

    @Override
    protected VCardDataType _defaultDataType(VCardVersion version) {
        return VCardDataType.TEXT;
    }

    @Override
    protected Telephone _parseText(String value, VCardDataType dataType,
                                   VCardParameters parameters, ParseContext context) {
        value = VObjectPropertyValues.unescape(value);
        return parse(value, dataType, context);
    }

    private Telephone parse(String value, VCardDataType dataType, ParseContext context) {
        Telephone tel;
        try {
            tel = new Telephone(TelUri.parse(value));
        } catch (IllegalArgumentException e) {
            if (dataType == VCardDataType.URI) {
                final int WARN = 18;
                context.addWarning(WARN);
            }
            tel = new Telephone(value);
        }
        return tel;
    }

    @Override
    protected String _writeText(Telephone property, WriteContext context) {
        String card = "";
        String text = property.getText();
        if (text != null) {
            card = escape(text, context);
        } else {
            TelUri uri = property.getUri();
            if (uri != null) {
                if (context.getVersion() == VCardVersion.V4_0) {
                    card = uri.toString();
                } else {
                    card = getCardNumber(uri, context);
                }
            }
        }
        return card;
    }

    private String getCardNumber(TelUri uri, WriteContext context) {
        String ext = uri.getExtension();
        String value;
        if (ext == null) {
            value = uri.getNumber();
        } else {
            value = uri.getNumber() + " x" + ext;
        }
        return escape(value, context);
    }

}
