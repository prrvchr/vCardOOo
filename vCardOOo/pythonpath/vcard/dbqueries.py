#!
# -*- coding: utf_8 -*-

"""
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
"""

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from .dbconfig import g_csv
from .configuration import g_member

from .logger import logMessage
from .logger import getMessage
g_message = 'dbqueries'


def getSqlQuery(ctx, name, format=None):

# Create Text Table Queries
    if name == 'createTextTable':
        query = 'CREATE TEXT TABLE IF NOT EXISTS "%s" (%s)' % format

    elif name == 'createTableTables':
        c1 = '"Table" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        c3 = '"Identity" INTEGER DEFAULT NULL'
        c4 = '"View" BOOLEAN DEFAULT TRUE'
        c5 = '"Versioned" BOOLEAN DEFAULT FALSE'
        k1 = 'CONSTRAINT "UniqueTablesName" UNIQUE("Name")'
        c = (c1, c2, c3, c4, c5, k1)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTableColumns':
        c1 = '"Column" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        k1 = 'CONSTRAINT "UniqueColumnsName" UNIQUE("Name")'
        c = (c1, c2, k1)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTableTableColumn':
        c1 = '"Table" INTEGER NOT NULL'
        c2 = '"Column" INTEGER NOT NULL'
        c3 = '"Type" VARCHAR(100) NOT NULL'
        c4 = '"Default" VARCHAR(100) DEFAULT NULL'
        c5 = '"Options" VARCHAR(100) DEFAULT NULL'
        c6 = '"Primary" BOOLEAN NOT NULL'
        c7 = '"Unique" BOOLEAN NOT NULL'
        c8 = '"ForeignTable" INTEGER DEFAULT NULL'
        c9 = '"ForeignColumn" INTEGER DEFAULT NULL'
        k1 = 'PRIMARY KEY("Table","Column")'
        k2 = 'CONSTRAINT "ForeignTableColumnTable" FOREIGN KEY("Table") REFERENCES '
        k2 += '"Tables"("Table") ON DELETE CASCADE ON UPDATE CASCADE'
        k3 = 'CONSTRAINT "ForeignTableColumnColumn" FOREIGN KEY("Column") REFERENCES '
        k3 += '"Columns"("Column") ON DELETE CASCADE ON UPDATE CASCADE'
        c = (c1, c2, c3, c4, c5, c6, c7, c8, c9, k1, k2, k3)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTableProperties':
        c1 = '"Property" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Value" VARCHAR(100) NOT NULL'
        c3 = '"Getter" VARCHAR(100) NOT NULL'
        c4 = '"Method" SMALLINT NOT NULL'
        c5 = '"View" VARCHAR(100) DEFAULT NULL'
        c = (c1, c2, c3, c4, c5)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTableParameters':
        c1 = '"Parameter" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Getter" VARCHAR(100) NOT NULL'
        c = (c1, c2)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTableTypes':
        c1 = '"Type" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Value" VARCHAR(100) NOT NULL'
        c3 = '"Column" VARCHAR(100) NOT NULL'
        c4 = '"Order" INTEGER NOT NULL'
        c = (c1, c2, c3, c4)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTablePropertyParameter':
        c1 = '"Property" INTEGER NOT NULL'
        c2 = '"Parameter" INTEGER NOT NULL'
        c3 = '"Column" VARCHAR(100)'
        c = (c1, c2, c3)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'createTablePropertyType':
        c1 = '"Property" INTEGER NOT NULL'
        c2 = '"Type" INTEGER NOT NULL'
        c3 = '"Group" INTEGER NOT NULL'
        c = (c1, c2, c3)
        f = (format, ','.join(c))
        query = getSqlQuery(ctx, 'createTextTable', f)

    elif name == 'setTableSource':
        query = 'SET TABLE "%s" SOURCE "%s"' % (format, g_csv % format)

    elif name == 'setTableHeader':
        query = 'SET TABLE "%s" SOURCE HEADER "%s"' % format

    elif name == 'setTableReadOnly':
        query = 'SET TABLE "%s" READONLY TRUE' % format

# Create Cached Table Options
    elif name == 'getPrimayKey':
        query = 'PRIMARY KEY(%s)' % ','.join(format)

    elif name == 'getUniqueConstraint':
        query = 'CONSTRAINT "Unique%(Table)s%(Column)s" UNIQUE("%(Column)s")' % format

    elif name == 'getForeignConstraint':
        q = 'CONSTRAINT "Foreign%(Table)s%(Column)s" FOREIGN KEY("%(Column)s") REFERENCES '
        q += '"%(ForeignTable)s"("%(ForeignColumn)s") ON DELETE CASCADE ON UPDATE CASCADE'
        query = q % format

# Create Cached Table Queries
    elif name == 'createTable':
        query = 'CREATE CACHED TABLE IF NOT EXISTS "%s"(%s)' % format

    elif name == 'getPeriodColumns':
        query = '"RowStart" TIMESTAMP(6) WITH TIME ZONE GENERATED ALWAYS AS ROW START,'
        query += '"RowEnd" TIMESTAMP(6) WITH TIME ZONE GENERATED ALWAYS AS ROW END,'
        query += 'PERIOD FOR SYSTEM_TIME("RowStart","RowEnd")'

    elif name == 'getSystemVersioning':
        query = ' WITH SYSTEM VERSIONING'

# Create Dynamic View Queries
    elif name == 'getAddressBookView':
        query = '''\
CREATE VIEW "%(View)s" ("%(Columns)s") AS SELECT %(Select)s FROM "Card" %(Table)s
''' % format

    elif name == 'createCardColumnsView':
        query = 'CREATE VIEW "AddressBook" (%(Columns)s) AS SELECT %(Select)s FROM %(Table)s' % format

    elif name == 'createView':
        query = 'CREATE VIEW "%s"(%s) AS SELECT %s FROM %s' % format

    elif name == 'getPrimaryColumnName':
        query = 'Resource'

    elif name == 'getBookmarkColumnName':
        query = 'Bookmark'

    elif name == 'getBookmarkColumn':
        query = 'ROW_NUMBER() OVER() AS "Bookmark"'

    elif name == 'getAddressBookTable':
        query = '''"Peoples"
JOIN "Connections" ON "Peoples"."People"="Connections"."People"
JOIN "Groups" ON "Connections"."Group"="Groups"."Group" AND "Groups"."GroupSync"=FALSE
JOIN "Peoples" AS P ON "Groups"."People"=P."People"
'''

    elif name == 'getAddressBookPredicate':
        query = '''WHERE P."Account"=CURRENT_USER OR CURRENT_USER='SA' ORDER BY "Peoples"."People"'''

    elif name == 'createGroupView':
        view = '''\
CREATE VIEW IF NOT EXISTS "%(Schema)s"."%(Name)s" AS
  SELECT "%(View)s".* FROM "%(View)s"
  JOIN "Peoples" ON "%(View)s"."Resource"="Peoples"."Resource"
  JOIN "Connections" ON "Peoples"."People"="Connections"."People"
  JOIN "Groups" ON "Connections"."Group"="Groups"."Group"
  WHERE "Groups"."Group"=%(GroupId)s ORDER BY "Peoples"."People";
GRANT SELECT ON "%(Schema)s"."%(Name)s" TO "%(User)s";
'''
        query = view % format

# Drop Dynamic View Queries
    elif name == 'dropGroupView':
        query = 'DROP VIEW IF EXISTS "%(Schema)s"."%(Name)s"' % format

# Create Trigger Query
    elif name == 'createTriggerUpdateAddressBook':
        query = 'CREATE TRIGGER "AddressBookUpdate" INSTEAD OF UPDATE ON "AddressBook" '
        query += 'REFERENCING NEW AS "new" OLD AS "old" FOR EACH ROW BEGIN ATOMIC %s END' % format

    elif name == 'createTriggerUpdateAddressBookCore':
        q = 'IF "new"."%(View)s" <> "old"."%(View)s" THEN '
        q += 'UPDATE "%(Table)s" SET "Value"="new"."%(View)s" WHERE '
        q += '"People"="new"."People" AND "Label"=%(LabelId)s'
        if format['TypeId'] is not None:
            q += ' AND "Type"=%(TypeId)s'
        q += '; END IF;'
        query = q % format

# Create User, Schema and Synonym Query
    elif name == 'createUser':
        q = """CREATE USER "%(User)s" PASSWORD '%(Password)s'"""
        if format.get('Admin', False):
            q += ' ADMIN;'
        else:
            q += ';'
        query = q % format

    elif name == 'createUserSchema':
        query = 'CREATE SCHEMA "%(Schema)s" AUTHORIZATION DBA;' % format

    elif name == 'setUserAuthorization':
        query = 'GRANT SELECT ON PUBLIC."%(View)s" TO "%(User)s";' % format

    elif name == 'createUserSynonym':
        query = 'CREATE SYNONYM "%(Schema)s"."%(View)s" FOR PUBLIC."%(View)s";' % format

    elif name == 'setUserSchema':
        query = 'ALTER USER "%(User)s" SET INITIAL SCHEMA "%(Schema)s"' % format

    elif name == 'setUserPassword':
        query = """ALTER USER "%(User)s" SET PASSWORD '%(Password)s'""" % format

# Get last IDENTITY value that was inserted into a table by the current session
    elif name == 'getIdentity':
        query = 'CALL IDENTITY();'

# Get Users and Privileges Query
    elif name == 'getUsers':
        query = 'SELECT * FROM INFORMATION_SCHEMA.SYSTEM_USERS'
    elif name == 'getPrivileges':
        query = 'SELECT * FROM INFORMATION_SCHEMA.TABLE_PRIVILEGES'
    elif name == 'changePassword':
        query = "SET PASSWORD '%s'" % format

# Select Queries
    # DataBase creation Select Queries
    elif name == 'getTableNames':
        query = 'SELECT "Name" FROM "Tables" ORDER BY "Table";'

    elif name == 'getTables':
        s1 = '"T"."Table" AS "TableId"'
        s2 = '"C"."Column" AS "ColumnId"'
        s3 = '"T"."Name" AS "Table"'
        s4 = '"C"."Name" AS "Column"'
        s5 = '"TC"."Type"'
        s6 = '"TC"."Default"'
        s7 = '"TC"."Options"'
        s8 = '"TC"."Primary"'
        s9 = '"TC"."Unique"'
        s10 = '"TC"."ForeignTable" AS "ForeignTableId"'
        s11 = '"TC"."ForeignColumn" AS "ForeignColumnId"'
        s12 = '"T2"."Name" AS "ForeignTable"'
        s13 = '"C2"."Name" AS "ForeignColumn"'
        s14 = '"T"."View"'
        s15 = '"T"."Versioned"'
        s = (s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15)
        f1 = '"Tables" AS "T"'
        f2 = 'JOIN "TableColumn" AS "TC" ON "T"."Table" = "TC"."Table"'
        f3 = 'JOIN "Columns" AS "C" ON "TC"."Column" = "C"."Column"'
        f4 = 'LEFT JOIN "Tables" AS "T2" ON "TC"."ForeignTable" = "T2"."Table"'
        f5 = 'LEFT JOIN "Columns" AS "C2" ON "TC"."ForeignColumn" = "C2"."Column"'
        w = '"T"."Name" = ?'
        f = (f1, f2, f3, f4, f5)
        p = (', '.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p


    elif name == 'getViewNames':
        query = 'SELECT "Name" FROM "Tables" WHERE "View"=TRUE ORDER BY "Table"'

    elif name == 'getViews':
        s1 = '"T1"."Table" AS "TableId"'
        s2 = '"TL"."Label" AS "LabelId"'
        s3 = '"TT"."Type" AS "TypeId"'
        s4 = '"T1"."Name" AS "Table"'
        s5 = '"L"."Name" AS "Label"'
        s6 = '"T"."Name" AS "Type"'
        s7 = 'CONCAT(COALESCE("T"."Name",\'\'),COALESCE("TL"."View","L"."Name")) AS "View"'
        s8 = '"T2"."Name" AS "PrimaryTable"'
        s9 = '"C"."Name" AS "PrimaryColumn"'
        s = (s1,s2,s3,s4,s5,s6,s7,s8,s9)
        f1 = '"Tables" AS "T1", "Tables" AS "T2"'
        f2 = 'JOIN "TableLabel" AS "TL" ON "T1"."Table"="TL"."Table"'
        f3 = 'JOIN "Labels" AS "L" ON "TL"."Label"="L"."Label"'
        f4 = 'LEFT JOIN "TableType" AS "TT" ON "T1"."Table"="TT"."Table"'
        f5 = 'LEFT JOIN "Types" AS "T" ON "TT"."Type"="T"."Type"'
        f6 = 'JOIN "Columns" AS "C" ON "T2"."Identity"="C"."Column"'
        w = '"T2"."Identity"=1 AND "T1"."Name"=? '
        f = (f1, f2, f3, f4, f5, f6)
        p = (','.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s ORDER BY "TableId","LabelId","TypeId"' % p

    elif name == 'getFieldNames':
        s = '"Fields"."Name"'
        f1 = '"Fields"'
        f2 = 'JOIN "Tables" ON "Fields"."Table"=%s AND "Fields"."Column"="Tables"."Table"'
        f = (f1, f2 % "'Tables'")
        w1 = '"Tables"."View"=TRUE'
        w2 = '"Fields"."Table"=%s AND "Fields"."Column"=1' % "'Loop'"
        p = (s, ' '.join(f), w1, s, f1, w2)
        query = 'SELECT %s FROM %s WHERE %s UNION SELECT %s FROM %s WHERE %s' % p

    elif name == 'getDefaultType':
        s1 = '"Tables"."Name" AS "Table"'
        s2 = '"Types"."Name" AS "Type"'
        s = (s1, s2)
        f1 = '"Tables"'
        f2 = 'JOIN "TableType" ON "Tables"."Table"="TableType"."Table"'
        f3 = 'JOIN "Types" ON "TableType"."Type"="Types"."Type"'
        w = '"TableType"."Default"=TRUE'
        f = (f1, f2 , f3 )
        p = (','.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p

    elif name == 'getFieldsMap':
        s1 = '"F"."Name" AS "Value"'
        s2 = 'COALESCE("Tables"."Name","Columns"."Name","Labels"."Name","Fields"."Name") AS "Name"'
        s3 = '"F"."Type"'
        s4 = '"F"."Table"'
        s = (s1, s2, s3, s4)
        f1 = '"Fields" AS "F"'
        f2 = 'LEFT JOIN "Tables" ON "F"."Table"=%s AND "F"."Column"="Tables"."Table"'
        f3 = 'LEFT JOIN "Columns" ON "F"."Table"=%s AND "F"."Column"="Columns"."Column"'
        f4 = 'LEFT JOIN "Labels" ON "F"."Table"=%s AND "F"."Column"="Labels"."Label"'
        f5 = 'LEFT JOIN "Fields" ON "F"."Table"=%s AND "F"."Field"="Fields"."Field"'
        f = (f1, f2 % "'Tables'", f3 % "'Columns'", f4 % "'Labels'", f5 % "'Loop'")
        p = (','.join(s), ' '.join(f))
        query = 'SELECT %s FROM %s WHERE "F"."Method"=? ORDER BY "F"."Field"' % p

    elif name == 'getPrimaryTable':
        s = 'COALESCE("Tables"."Name","Columns"."Name","Labels"."Name","Fields"."Name") AS "Name"'
        f1 = '"Fields" AS "F"'
        f2 = 'LEFT JOIN "Tables" ON "F"."Table"=%s AND "F"."Column"="Tables"."Table"'
        f3 = 'LEFT JOIN "Columns" ON "F"."Table"=%s AND "F"."Column"="Columns"."Column"'
        f4 = 'LEFT JOIN "Labels" ON "F"."Table"=%s AND "F"."Column"="Labels"."Label"'
        f5 = 'LEFT JOIN "Fields" ON "F"."Table"=%s AND "F"."Field"="Fields"."Field"'
        f = (f1, f2 % "'Tables'", f3 % "'Columns'", f4 % "'Labels'", f5 % "'Loop'")
        w = '"F"."Type"=%s AND "F"."Table"=%s' % ("'Primary'","'Tables'")
        p = (s, ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p


    elif name == 'getUser':
        c = '"User","Default","Scheme","Server","Path","Name"'
        f = '"Users"'
        w = '"Server" = ? AND "Name" = ?'
        query = 'SELECT %s FROM %s WHERE %s' % (c, f, w)


    elif name == 'getPerson1':
        c = '"People","Group","Resource","Account","PeopleSync","GroupSync"'
        f = '"Peoples" JOIN "Groups"'
        o1 = '"Peoples"."People"="Groups"."People"'
        o2 = '"Peoples"."Resource"="Groups"."Resource"'
        w = '"Peoples"."Account"=?'
        query = 'SELECT %s FROM %s ON %s AND %s WHERE %s' % (c, f, o1, o2, w)

    elif name == 'getUpdatedGroup':
        query = 'SELECT "Resource" FROM "Groups" FOR SYSTEM_TIME AS OF CURRENT_TIMESTAMP - 1 YEAR'

# Update Queries
    elif name == 'updateAddressbookToken':
        query = 'UPDATE "Addressbooks" SET "Token"=?,"Modified"=DEFAULT WHERE "Addressbook"=?'


    elif name == 'updateUser':
        query = 'UPDATE "Users" SET "Scheme"=?,"Password"=? WHERE "User"=?'

    elif name == 'updateUserScheme':
        query = 'UPDATE "Users" SET "Scheme"=? WHERE "User"=?'

    elif name == 'updateUserPassword':
        query = 'UPDATE "Users" SET "Password"=? WHERE "User"=?'


    elif name == 'updatePeoples':
        query = 'UPDATE "Peoples" SET "TimeStamp"=? WHERE "Resource"=?'

    elif name == 'updatePeopleSync':
        query = 'UPDATE "Peoples" SET "PeopleSync"=?,"TimeStamp"=? WHERE "People"=?'

    elif name == 'updateGroupSync':
        query = 'UPDATE "Peoples" SET "GroupSync"=?,"TimeStamp"=? WHERE "People"=?'

# Get DataBase Version Query
    elif name == 'getVersion':
        query = 'Select DISTINCT DATABASE_VERSION() as "HSQL Version" From INFORMATION_SCHEMA.SYSTEM_TABLES'

# Create Trigger Query
    elif name == 'createTriggerGroupInsert':
        query = """\
CREATE TRIGGER "GroupInsert" AFTER INSERT ON "Groups"
  REFERENCING NEW ROW AS "NewRow"
  FOR EACH ROW
  BEGIN ATOMIC
    CALL "GroupView" ("NewRow"."Name", "NewRow"."Group")
  END"""

    elif name == 'selectUpdatedGroup':
        c1 = '?||"Resource" AS "Resource"'
        c2 = '"Group"'
        c3 = '"Name"'
        q = '\
SELECT %s FROM "Groups" WHERE "GroupSync"=FALSE AND "People"=? AND "Resource"<>?'
        query = q % ','.join((c1, c2, c3))

    elif name == 'truncatGroup':
        q = """\
TRUNCATE TABLE "Groups" VERSIONING TO TIMESTAMP'%(TimeStamp)s'"""
        query = q % format

# Insert Queries
    elif name == 'insertSuperUser':
        q = """\
INSERT INTO "Users" ("Scheme","Server","Path","Name") VALUES ('%s','%s','%s','%s');
"""
        query = q % format

# Create Procedure Query
    elif name == 'createSelectGroup':
        query = """\
CREATE PROCEDURE "SelectGroup"(IN "Prefix" VARCHAR(50),
                               IN "PeopleId" INTEGER,
                               IN "ResourceName" VARCHAR(100))
  SPECIFIC "SelectGroup_1"
  READS SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE "StartTime","EndTime","Format" VARCHAR(30);
    DECLARE "TmpTime" TIMESTAMP(6);
    DECLARE "Result" CURSOR WITH RETURN FOR
      SELECT "Prefix"||"Resource" FROM "Groups" FOR SYSTEM_TIME FROM 
      TO_TIMESTAMP('%(Start)s','%(Format)s') TO TO_TIMESTAMP('%(End)s','%(Format)s')
      WHERE "People"="PeopleId" AND "Resource"<>"ResourceName" FOR READ ONLY;
    SET "Time" = LOCALTIMESTAMP(6);
    SET "TmpTime" = "Time" - 10 MINUTE;
    SET "Format" = 'YYYY-MM-DDTHH24:MI:SS.FFFZ';
    SET "EndTime" = TO_CHAR("Time","Format");
    SET "StartTime" = TO_CHAR("TmpTime","Format");
    SET "Time" = "EndTime";
    OPEN "Result";
  END"""

    elif name == 'createInsertUser':
        query = """\
CREATE PROCEDURE "InsertUser"(IN SCHEME VARCHAR(128),
                              IN SERVER VARCHAR(128),
                              IN PATH VARCHAR(256),
                              IN UID VARCHAR(128),
                              IN URL VARCHAR(256),
                              IN NAME VARCHAR(128),
                              IN TAG VARCHAR(128),
                              IN TOKEN VARCHAR(128))
  SPECIFIC "InsertUser_1"
  MODIFIES SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE PK1,PK2 INTEGER DEFAULT NULL;
    DECLARE RSLT CURSOR WITH RETURN FOR
      SELECT "User","Default","Scheme","Server","Path","Name"
      FROM "Users"
      WHERE "Server"=SERVER AND "Name"=UID FOR READ ONLY;
    INSERT INTO "Users" ("Scheme","Server","Path","Name") VALUES (SCHEME,SERVER,PATH,UID);
    SET PK1=IDENTITY();
    INSERT INTO "Addressbooks" ("User","Path","Name","Tag","Token") VALUES (PK1,URL,NAME,TAG,TOKEN);
    SET PK2=IDENTITY();
    INSERT INTO "Groups" ("Addressbook") VALUES (PK2);
    UPDATE "Users" SET "Default"=PK2 WHERE "User"=PK1;
    OPEN RSLT;
  END"""

    elif name == 'createSelectAddressbook':
        query = """\
CREATE PROCEDURE "SelectAddressbook"(IN UID INTEGER,
                                     IN AID INTEGER,
                                     IN NAME VARCHAR(128))
  SPECIFIC "SelectAddressbook_1"
  READS SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE RSLT CURSOR WITH RETURN FOR
      SELECT A."Addressbook", G."Group", A."Path", A."Name",A."Tag",
      A."Token" AS "AdrSync", G."Token" AS "GrpSync",
      A."Created"=A."Modified" AS "New"
      FROM "Users" AS U
      JOIN "Addressbooks" AS A ON U."User"=A."User"
      JOIN "Groups" AS G ON A."Addressbook"=G."Addressbook" AND G."Name" IS NULL
      WHERE U."User"=UID AND (A."Addressbook"=AID OR
        (((NAME IS NULL AND A."Addressbook"=U."Default") OR
        (NAME IS NOT NULL AND A."Name"=NAME))))
      FOR READ ONLY;
    OPEN RSLT;
  END"""

    elif name == 'createInsertAddressbook':
        query = """\
CREATE PROCEDURE "InsertAddressbook"(IN UID INTEGER,
                                     IN PATH VARCHAR(256),
                                     IN NAME VARCHAR(128),
                                     IN TAG VARCHAR(128),
                                     IN TOKEN VARCHAR(128))
  SPECIFIC "InsertAddressbook_1"
  MODIFIES SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE RSLT CURSOR WITH RETURN FOR
      SELECT A."Addressbook",G."Group",A."Path",A."Name",A."Tag",
      A."Token" AS "AdrSync",G."Token" AS "GrpSync",
      A."Created"=A."Modified" AS "New"
      FROM "Addressbooks" AS A
      JOIN "Groups" AS G ON A."Addressbook"=G."Addressbook" AND G."Name" IS NULL
      WHERE A."User"=UID AND A."Name"=NAME FOR READ ONLY;
    INSERT INTO "Addressbooks" ("User","Path","Name","Tag","Token") VALUES (UID,PATH,NAME,TAG,TOKEN);
    INSERT INTO "Groups" ("Addressbook") VALUES (IDENTITY());
    OPEN RSLT;
  END"""

    elif name == 'createMergeCard':
        query = """\
CREATE PROCEDURE "MergeCard"(IN AID INTEGER,
                             IN PATH VARCHAR(256),
                             IN TAG VARCHAR(128),
                             IN DATA VARCHAR(100000))
  SPECIFIC "MergeCard_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    MERGE INTO "Cards" USING (VALUES(AID,PATH,TAG,DATA))
      AS vals(w,x,y,z) ON "Cards"."Addressbook"=vals.w AND "Cards"."Path"=vals.x
        WHEN MATCHED THEN UPDATE SET "Tag"=vals.y,"Data"=vals.z
        WHEN NOT MATCHED THEN INSERT ("Addressbook","Path","Tag","Data")
          VALUES vals.w,vals.x,vals.y,vals.z;
  END"""

    elif name == 'createDeleteCard':
        query = """\
CREATE PROCEDURE "DeleteCard"(IN AID INTEGER,
                              IN URLS VARCHAR(256) ARRAY)
  SPECIFIC "DeleteCard_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DELETE FROM "Cards" WHERE "Addressbook"=AID AND "Path" IN (UNNEST(URLS));
  END"""

    elif name == 'createSelectChangedCards':
        query = """\
CREATE PROCEDURE "SelectChangedCards"(INOUT FIRST TIMESTAMP(6) WITH TIME ZONE,
                                      INOUT LAST TIMESTAMP(6) WITH TIME ZONE)
  SPECIFIC "SelectChangedCards_1"
  MODIFIES SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE RSLT CURSOR WITH RETURN FOR
      (SELECT U1."User",C1."Card",NULL AS "Data",'Deleted' AS "Query",C1."RowEnd" AS "Order"
      FROM "Cards" FOR SYSTEM_TIME AS OF FIRST AS C1
      JOIN "Addressbooks" AS A ON C1."Addressbook"=A."Addressbook"
      JOIN "Users" AS U1 ON A."User"=U1."User"
      LEFT JOIN "Cards" FOR SYSTEM_TIME AS OF LAST AS C2
        ON C1."Card" = C2."Card"
      WHERE C2."Card" IS NULL)
      UNION
      (SELECT U2."User",C2."Card",C2."Data",'Inserted' AS "Query",C2."RowStart" AS "Order"
      FROM "Cards" FOR SYSTEM_TIME AS OF LAST AS C2
      JOIN "Addressbooks" AS A ON C2."Addressbook"=A."Addressbook"
      JOIN "Users" AS U2 ON A."User"=U2."User"
      LEFT JOIN "Cards" FOR SYSTEM_TIME AS OF FIRST AS C1
        ON C2."Card"=C1."Card"
      WHERE C1."Card" IS NULL)
      UNION
      (SELECT U3."User",C2."Card",C2."Data",'Updated' AS "Query",C1."RowEnd" AS "Order"
      FROM "Cards" FOR SYSTEM_TIME AS OF LAST AS C2
      JOIN "Addressbooks" AS A ON C2."Addressbook"=A."Addressbook"
      JOIN "Users" AS U3 ON A."User"=U3."User"
      INNER JOIN "Cards" FOR SYSTEM_TIME FROM FIRST TO LAST AS C1
        ON C2."Card"=C1."Card" AND C2."RowStart"=C1."RowEnd")
      ORDER BY "Order"
      FOR READ ONLY;
    UPDATE "Users" SET "Modified"=DEFAULT WHERE "User"=0;
    SET (FIRST, LAST) = (SELECT "Created", "Modified" FROM "Users" WHERE "User"=0);
    OPEN RSLT;
  END"""

    elif name == 'createUpdateUser':
        query = """\
CREATE PROCEDURE "UpdateUser"()
  SPECIFIC "UpdateUser_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE DATETIME TIMESTAMP(6) WITH TIME ZONE;
    SET DATETIME = (SELECT "Modified" FROM "Users" WHERE "User"=0);
    UPDATE "Users" SET "Created"=DATETIME WHERE "User"=0;
  END"""

    elif name == 'createSelectAddressbookColumns':
        query = """\
CREATE PROCEDURE "SelectAddressbookColumns"()
  SPECIFIC "SelectAddressbookColumns_1"
  READS SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE RSLT CURSOR WITH RETURN FOR
      SELECT ROWNUM() AS "ColumnId",
        C."Value" AS "PropertyName",
        C."View" AS "ViewName",
        C."Getter" AS "PropertyGetter",
        P."Getter" AS "ParameterGetter",
        C."Method",
        COALESCE(GROUP_CONCAT(T."Column" ORDER BY T."Order" SEPARATOR ''),'') ||
        COALESCE(PP."Column",'') AS "ColumnName",
        ARRAY_AGG(T."Value") AS "TypeValues"
      FROM "Properties" AS C
      JOIN "PropertyParameter" AS PP ON C."Property"=PP."Property"
      JOIN "Parameters" AS P ON PP."Parameter"=P."Parameter"
      LEFT JOIN "PropertyType" AS PT ON C."Property"=PT."Property"
      LEFT JOIN "Types" AS T ON PT."Type"=T."Type"
      GROUP BY C."Value",C."View",C."Getter",P."Getter",C."Typed",PP."Column",PT."Group"
      FOR READ ONLY;
    OPEN RSLT;
  END"""

    elif name == 'createMergeCardValue':
        query = """\
CREATE PROCEDURE "MergeCardValue"(IN AID INTEGER,
                                  IN CID INTEGER,
                                  IN DATA VARCHAR(128))
  SPECIFIC "MergeCardValue_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    MERGE INTO "CardValues" USING (VALUES(AID,CID,DATA))
      AS vals(x,y,z) ON "Card"=vals.x AND "Column"=vals.y
        WHEN MATCHED THEN UPDATE SET "Value"=vals.z
        WHEN NOT MATCHED THEN INSERT ("Card","Column","Value")
          VALUES vals.x,vals.y,vals.z;
  END"""


    elif name == 'createInsertUser1':
        query = """\
CREATE PROCEDURE "InsertUser"(IN "ResourceName" VARCHAR(100),
                              IN "UserName" VARCHAR(100),
                              IN "GroupName" VARCHAR(100))
  SPECIFIC "InsertUser_1"
  MODIFIES SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE "Result" CURSOR WITH RETURN FOR
      SELECT "People", "Group", "Resource", "Account", "PeopleSync", "GroupSync"
      FROM "Peoples" JOIN "Groups" ON "Peoples"."People"="Groups"."People"
      AND "Peoples"."Resource"="Groups"."Resource"
      WHERE "Peoples"."Resource"="ResourceName" FOR READ ONLY;
    INSERT INTO "Peoples" ("Resource","Account") VALUES ("ResourceName","UserName");
    INSERT INTO "Groups" ("People","Resource","Name")
      VALUES (IDENTITY(),"ResourceName","GroupName");
    OPEN "Result";
  END"""

    elif name == 'createGetPeopleIndex':
        query = """\
CREATE FUNCTION "GetPeopleIndex"("Prefix" VARCHAR(50),"ResourceName" VARCHAR(100))
  RETURNS INTEGER
  SPECIFIC "GetPeopleIndex_1"
  READS SQL DATA
  RETURN (SELECT "People" FROM "Peoples" WHERE "Prefix"||"Resource"="ResourceName");
"""

    elif name == 'createGetLabelIndex':
        query = """\
CREATE FUNCTION "GetLabelIndex"("LabelName" VARCHAR(100))
  RETURNS INTEGER
  SPECIFIC "GetLabelIndex_1"
  READS SQL DATA
  RETURN (SELECT "Label" FROM "Labels" WHERE "Name"="LabelName");
"""

    elif name == 'createGetTypeIndex':
        query = """\
CREATE PROCEDURE "GetTypeIndex"(IN "TableName" VARCHAR(100),
                                IN "TypeName" VARCHAR(100),
                                OUT "TypeId" INTEGER)
  SPECIFIC "GetTypeIndex_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "TypeIndex" INTEGER DEFAULT NULL;
    SET "TypeIndex" = SELECT "Type" FROM "Types" WHERE "Name"="TypeName";
    IF "TypeIndex" IS NULL THEN
      SET "TypeIndex" = SELECT "Type" FROM "TableType" JOIN "Tables"
        ON "TableType"."Table"="Tables"."Table"
          WHERE "TableType"."Default"=TRUE AND "Tables"."Name"="TableName";
      IF "TypeIndex" IS NULL THEN 
        INSERT INTO "Types" ("Name","Value") VALUES ("TypeName","TypeName");
        SET "TypeIndex" = IDENTITY();
      END IF;
    END IF;
    SET "TypeId" = "TypeIndex";
  END"""

    elif name == 'createMergePeople':
        query = """\
CREATE PROCEDURE "MergePeople"(IN "Prefix" VARCHAR(50),
                               IN "ResourceName" VARCHAR(100),
                               IN "GroupId" INTEGER,
                               IN "Time" TIMESTAMP(6),
                               IN "Deleted" BOOLEAN)
  SPECIFIC "MergePeople_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleResource" VARCHAR(100);
    SET "PeopleResource" = REPLACE("ResourceName", "Prefix");
    IF "Deleted"=TRUE THEN
      DELETE FROM "Peoples" WHERE "Resource"="PeopleResource";
    ELSEIF NOT EXISTS(SELECT "People" FROM "Peoples" WHERE "Resource"="PeopleResource") THEN 
      INSERT INTO "Peoples" ("Resource","TimeStamp") VALUES ("PeopleResource","Time");
      INSERT INTO "Connections" ("Group","People","TimeStamp") VALUES ("GroupId",IDENTITY(),"Time");
    END IF;
  END"""

    elif name == 'createUnTypedDataMerge':
        q = """\
CREATE PROCEDURE "Merge%(Table)s"(IN "Prefix" VARCHAR(50),
                                  IN "ResourceName" VARCHAR(100),
                                  IN "LabelName" VARCHAR(100),
                                  IN "Value" VARCHAR(100),
                                  IN "Time" TIMESTAMP(6))
  SPECIFIC "Merge%(Table)s_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleIndex","LabelIndex" INTEGER DEFAULT NULL;
    SET "PeopleIndex" = "GetPeopleIndex"("Prefix","ResourceName");
    SET "LabelIndex" = "GetLabelIndex"("LabelName");
    MERGE INTO "%(Table)s" USING
      (VALUES("PeopleIndex","LabelIndex","Value","Time")) AS vals(w,x,y,z)
      ON "%(Table)s"."People"=vals.w AND "%(Table)s"."Label"=vals.x
        WHEN MATCHED THEN UPDATE SET "Value"=vals.y, "TimeStamp"=vals.z
        WHEN NOT MATCHED THEN INSERT ("People","Label","Value","TimeStamp")
          VALUES vals.w, vals.x, vals.y, vals.z;
  END"""
        query = q % format

    elif name == 'createTypedDataMerge':
        q = """\
CREATE PROCEDURE "Merge%(Table)s"(IN "Prefix" VARCHAR(50),
                                  IN "ResourceName" VARCHAR(100),
                                  IN "LabelName" VARCHAR(100),
                                  IN "Value" VARCHAR(100),
                                  IN "Time" TIMESTAMP(6),
                                  IN "Table" VARCHAR(50),
                                  IN "TypeName" VARCHAR(100))
  SPECIFIC "Merge%(Table)s_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleIndex","TypeIndex","LabelIndex" INTEGER DEFAULT NULL;
    SET "PeopleIndex" = "GetPeopleIndex"("Prefix","ResourceName");
    CALL "GetTypeIndex"("Table","TypeName","TypeIndex");
    SET "LabelIndex" = "GetLabelIndex"("LabelName");
    MERGE INTO "%(Table)s" USING
      (VALUES("PeopleIndex","TypeIndex","LabelIndex","Value","Time")) AS vals(v,w,x,y,z)
      ON "%(Table)s"."People"=vals.v AND "%(Table)s"."Type"=vals.w AND "%(Table)s"."Label"=vals.x
        WHEN MATCHED THEN UPDATE SET "Value"=vals.y, "TimeStamp"=vals.z
        WHEN NOT MATCHED THEN INSERT ("People","Type","Label","Value","TimeStamp")
          VALUES vals.v, vals.w, vals.x, vals.y, vals.z;
  END"""
        query = q % format

    elif name == 'createMergeGroup':
        query = """\
CREATE PROCEDURE "MergeGroup"(IN "Prefix" VARCHAR(50),
                              IN "PeopleId" INTEGER,
                              IN "ResourceName" VARCHAR(100),
                              IN "GroupName" VARCHAR(100),
                              IN "Time" TIMESTAMP(6),
                              IN "Deleted" BOOLEAN)
  SPECIFIC "MergeGroup_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "GroupResource" VARCHAR(100);
    SET "GroupResource" = REPLACE("ResourceName", "Prefix");
    IF "Deleted"=TRUE THEN
      DELETE FROM "Groups" WHERE "People"="PeopleId" AND "Resource"="GroupResource";
    ELSE
      MERGE INTO "Groups" USING (VALUES("PeopleId","GroupResource","GroupName","Time"))
        AS vals(w,x,y,z) ON "Groups"."Resource"=vals.x
          WHEN MATCHED THEN UPDATE
            SET "People"=vals.w, "Name"=vals.y, "TimeStamp"=vals.z, "GroupSync"=FALSE
          WHEN NOT MATCHED THEN INSERT ("People","Resource","Name","TimeStamp")
            VALUES vals.w, vals.x, vals.y, vals.z;
    END IF;
  END"""

    elif name == 'createMergeConnection':
        q = """\
CREATE PROCEDURE "MergeConnection"(IN "GroupPrefix" VARCHAR(50),
                                   IN "PeoplePrefix" VARCHAR(50),
                                   IN "ResourceName" VARCHAR(100),
                                   IN "Time" TIMESTAMP(6),
                                   IN "Separator" VARCHAR(1),
                                   IN "MembersList" VARCHAR(15000))
  SPECIFIC "MergeConnection_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "Index" INTEGER DEFAULT 1;
    DECLARE "Pattern" VARCHAR(5) DEFAULT '[^$]+';
    DECLARE "GroupId", "PeopleId" INTEGER;
    DECLARE "GroupResource", "PeopleResource" VARCHAR(100);
    DECLARE "MembersArray" VARCHAR(100) ARRAY[%s];
    SET "GroupResource" = REPLACE("ResourceName", "GroupPrefix");
    SELECT "Group" INTO "GroupId" FROM "Groups" WHERE "Resource"="GroupResource";
    DELETE FROM "Connections" WHERE "Group"="GroupId";
    SET "Pattern" = REPLACE("Pattern", '$', "Separator");
    SET "MembersArray" = REGEXP_SUBSTRING_ARRAY("MembersList", "Pattern");
    WHILE "Index" <= CARDINALITY("MembersArray") DO
      SET "PeopleResource" = REPLACE("MembersArray"["Index"], "PeoplePrefix");
      SELECT "People" INTO "PeopleId" FROM "Peoples" WHERE "Resource"="PeopleResource";
      INSERT INTO "Connections" ("Group","People","TimeStamp")
        VALUES ("GroupId","PeopleId","Time");
      SET "Index" = "Index" + 1;
    END WHILE;
    UPDATE "Groups" SET "GroupSync"=TRUE WHERE "Group"="GroupId";
  END"""
        query = q % g_member

# Get Procedure Query
    elif name == 'insertUser':
        query = 'CALL "InsertUser"(?,?,?,?,?,?,?,?)'
    elif name == 'selectAddressbook':
        query = 'CALL "SelectAddressbook"(?,?,?)'
    elif name == 'insertAddressbook':
        query = 'CALL "InsertAddressbook"(?,?,?,?,?)'
    elif name == 'mergeCard':
        query = 'CALL "MergeCard"(?,?,?,?)'
    elif name == 'deleteCard':
        query = 'CALL "DeleteCard"(?,?)'
    elif name == 'getAddressbookColumns':
        query = 'CALL "SelectAddressbookColumns"()'

    elif name == 'mergePeople':
        query = 'CALL "MergePeople"(?,?,?,?,?)'
    elif name == 'mergeGroup':
        query = 'CALL "MergeGroup"(?,?,?,?,?,?)'
    elif name == 'mergeConnection':
        query = 'CALL "MergeConnection"(?,?,?,?,?,?)'
    elif name == 'mergePeopleData':
        if format['Type'] is None:
            q = 'CALL "Merge%(Table)s"(?,?,?,?,?)'
        else:
            q = 'CALL "Merge%(Table)s"(?,?,?,?,?,?,?)'
        query = q % format

# Logging Changes Queries
    elif name == 'loggingChanges':
        if format:
            query = 'SET FILES LOG TRUE'
        else:
            query = 'SET FILES LOG FALSE'

# Saves Changes Queries
    elif name == 'saveChanges':
        if format:
            query = 'CHECKPOINT DEFRAG'
        else:
            query = 'CHECKPOINT'

# ShutDown Queries
    elif name == 'shutdown':
        if format:
            query = 'SHUTDOWN COMPACT;'
        else:
            query = 'SHUTDOWN;'

    elif name == 'shutdownCompact':
        query = 'SHUTDOWN COMPACT;'

# Queries don't exist!!!
    else:
        query = None
        msg = getMessage(ctx, g_message, 101, name)
        logMessage(ctx, SEVERE, msg, 'dbqueries', 'getSqlQuery()')
    return query
