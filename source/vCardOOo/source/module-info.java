module io.github.prrvchr.vcard {
    requires transitive io.github.prrvchr.unohelper;
    requires transitive org.libreoffice.uno;
    requires transitive org.json;
    requires ez.vcard;

    exports io.github.prrvchr.carddav;
}