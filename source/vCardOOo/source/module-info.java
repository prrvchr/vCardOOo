module io.github.prrvchr.vcard {
    requires transitive io.github.prrvchr.unohelper;
    requires transitive org.json;
    requires ezVcard;

    exports io.github.prrvchr.carddav;
}