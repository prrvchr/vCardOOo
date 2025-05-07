module ezVcard {
    requires java.xml;
    requires transitive vinnie;
    requires transitive com.fasterxml.jackson.core;
    requires transitive com.fasterxml.jackson.databind;
    requires transitive org.jsoup;
    requires transitive freemarker;

    exports ezvcard;
    exports ezvcard.io;
    exports ezvcard.io.chain;
    exports ezvcard.io.html;
    exports ezvcard.io.json;
    exports ezvcard.io.scribe;
    exports ezvcard.io.text;
    exports ezvcard.io.xml;
    exports ezvcard.parameter;
    exports ezvcard.property;
    exports ezvcard.util;
}