module io.github.prrvchr.vcard {
    requires transitive io.github.prrvchr.unohelper;
    requires transitive org.json;
    requires transitive org.libreoffice.uno;
    requires ezVcard;

    exports io.github.prrvchr.carddav;
}