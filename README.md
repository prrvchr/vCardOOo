# Documentation

**Ce [document][1] en français.**

**The use of this software subjects you to our [Terms Of Use][2] and [Data Protection Policy][3].**

# version [1.0.3][4]

## Introduction:

**vCardOOo** is part of a [Suite][5] of [LibreOffice][6] ~~and/or [OpenOffice][7]~~ extensions allowing to offer you innovative services in these office suites.  
This extension gives you access, in LibreOffice, to your contacts present on a CardDAV server (or vCard Extensions to WebDAV).

Being free software I encourage you:
- To duplicate its [source code][8].
- To make changes, corrections, improvements.
- To open [issue][9] if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

___

## Requirement:

In order to take advantage of the latest versions of the Python libraries used in vCardOOo, version 2 of Python has been abandoned in favor of **Python 3.8 minimum**.  
This means that **vCardOOo no longer supports OpenOffice and LibreOffice 6.x on Windows since version 1.0.0**.
I can only advise you **to migrate to LibreOffice 7.x**.

vCardOOo uses a local [HsqlDB][10] database version 2.7.2.  
HsqlDB being a database written in Java, its use requires the [installation and configuration][11] in LibreOffice / OpenOffice of a **JRE version 11 or later**.  
I recommend [Adoptium][12] as your Java installation source.

If you are using **LibreOffice Community on Linux**, you are subject to [bug 139538][13]. To work around the problem, please **uninstall the packages** with commands:
- `sudo apt remove libreoffice-sdbc-hsqldb` (to uninstall the libreoffice-sdbc-hsqldb package)
- `sudo apt remove libhsqldb1.8.0-java` (to uninstall the libhsqldb1.8.0-java package)

If you still want to use the Embedded HsqlDB functionality provided by LibreOffice, then install the [HyperSQLOOo][14] extension.  

___

## Installation:

It seems important that the file was not renamed when it was downloaded.
If necessary, rename it before installing it.

- Install ![OAuth2OOo logo][15] **[OAuth2OOo.oxt][16]** extension [![Version][17]][16]

    You must install this extension, if it is not already installed.

- Install ![jdbcDriverOOo logo][18] **[jdbcDriverOOo.oxt][19]** extension [![Version][20]][19]

    You must install this extension, if it is not already installed.

- Install ![vCardOOo logo][21] **[vCardOOo.oxt][22]** extension [![Version][23]][22]

Restart LibreOffice / OpenOffice after installation.

___

## Use:

In LibreOffice / OpenOffice go to File -> Wizards -> Address Data Source...:

![vCardOOo screenshot 1][24]

In step: 1. Address Book Type:
- select: Other external data source
- click on: Next(Button)

![vCardOOo screenshot 2][25]

In step: 2. Connection Settings:
- click on: Settings(Button)

![vCardOOo screenshot 3][26]

In Database type list:
- select: vCard Contacts
- click on: Next(Button)

![vCardOOo screenshot 4][27]

In General: Datasource Url:
- put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In General: User:
- put your username.

In General: Password:
- put your password.

Then:
- click on: Test connection (button)

![vCardOOo screenshot 5][28]

![vCardOOo screenshot 6][29]

![vCardOOo screenshot 7][30]

![vCardOOo screenshot 8][31]

![vCardOOo screenshot 9][32]

![vCardOOo screenshot 10][33]

![vCardOOo screenshot 11][34]

Have fun...

___

## Has been tested with:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* **Does not work with OpenOffice on Windows** see [bug 128569][35]. Having no solution, I encourage you to install **LibreOffice**.

I encourage you in case of problem :confused:  
to create an [issue][9]  
I will try to solve it :smile:

___

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your address book) stored in your Android phone.

With the [eMailerOOo][36] extension, it can be the data source for [mail merge][37] by email, to your correspondents contained in your phone.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver][38] responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource][39] singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator][40] thread to track remote changes on Nextcloud servers.
  - Create and cache a [User][41] Interface needed for:
    - Creating the connection to the underlying database.
    - Connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync][42] written in Java and using the [ez-vcard][43] library.

### What has been done for version 1.0.1:

- The absence or obsolescence of the **OAuth2OOo** and/or **jdbcDriverOOo** extensions necessary for the proper functioning of **vCardOOo** now displays an error message.

- Many other things...

### What has been done for version 1.0.2:

- Support for version **1.2.0** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.0 or higher.

### What has been done for version 1.0.3:

- Support for version **1.2.1** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.1 or higher.

### What remains to be done for version 1.0.3:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...

[1]: <https://prrvchr.github.io/vCardOOo/README_fr>
[2]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_en>
[3]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_en>
[4]: <https://prrvchr.github.io/vCardOOo#historical>
[5]: <https://prrvchr.github.io/>
[6]: <https://www.libreoffice.org/download/download/>
[7]: <https://www.openoffice.org/download/index.html>
[8]: <https://github.com/prrvchr/vCardOOo>
[9]: <https://github.com/prrvchr/vCardOOo/issues/new>
[10]: <http://hsqldb.org/>
[11]: <https://wiki.documentfoundation.org/Documentation/HowTo/Install_the_correct_JRE_-_LibreOffice_on_Windows_10>
[12]: <https://adoptium.net/releases.html?variant=openjdk11>
[13]: <https://bugs.documentfoundation.org/show_bug.cgi?id=139538>
[14]: <https://prrvchr.github.io/HyperSQLOOo/>
[15]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[16]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[17]: <https://img.shields.io/github/downloads/prrvchr/OAuth2OOo/latest/total?label=v1.2.1#right>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[20]: <https://img.shields.io/github/downloads/prrvchr/jdbcDriverOOo/latest/total?label=v1.0.5#right>
[21]: <img/vCardOOo.svg#middle>
[22]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[23]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.0.3#right>
[24]: <img/vCardOOo-1.png>
[25]: <img/vCardOOo-2.png>
[26]: <img/vCardOOo-3.png>
[27]: <img/vCardOOo-4.png>
[28]: <img/vCardOOo-5.png>
[29]: <img/vCardOOo-6.png>
[30]: <img/vCardOOo-7.png>
[31]: <img/vCardOOo-8.png>
[32]: <img/vCardOOo-9.png>
[33]: <img/vCardOOo-10.png>
[34]: <img/vCardOOo-11.png>
[35]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[36]: <https://prrvchr.github.io/eMailerOOo/>
[37]: <https://en.wikipedia.org/wiki/Mail_merge>
[38]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[39]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[40]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[41]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[42]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[43]: <https://github.com/mangstadt/ez-vcard>
