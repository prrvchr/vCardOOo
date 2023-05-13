# ![vCardOOo logo][1] vCardOOo

**Ce [document][2] en français.**

**The use of this software subjects you to our** [**Terms Of Use**][3] **and** [**Data Protection Policy**][4]

# version [0.0.1][5]

## Introduction:

**vCardOOo** is part of a [Suite][6] of [LibreOffice][7] and/or [OpenOffice][8] extensions allowing to offer you innovative services in these office suites.  
This extension gives you access to your phone contacts in LibreOffice / OpenOffice (the contacts of your Android phone).

Being free software I encourage you:
- To duplicate its [source code][9].
- To make changes, corrections, improvements.
- To open [issue][10] if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

## Requirement:

vCardOOo uses a local [HsqlDB][11] database version 2.5.1.  
HsqlDB being a database written in Java, its use requires the [installation and configuration][12] in LibreOffice / OpenOffice of a **JRE version 11 or later**.  
I recommend [Adoptium][13] as your Java installation source.

If you are using **LibreOffice on Linux**, then you are subject to [bug 139538][14].  
To work around the problem, please uninstall the packages:
- libreoffice-sdbc-hsqldb
- libhsqldb1.8.0-java

If you still want to use the Embedded HsqlDB functionality provided by LibreOffice, then install the [HsqlDBembeddedOOo][15] extension.  
OpenOffice and LibreOffice on Windows are not subject to this malfunction.

## Installation:

It seems important that the file was not renamed when it was downloaded.
If necessary, rename it before installing it.

- Install ![OAuth2OOo logo][16] **[OAuth2OOo.oxt][17]** extension version 0.0.5.

You must install this extension, if it is not already installed.

- Install ![jdbcDriverOOo logo][18] **[jdbcDriverOOo.oxt][19]** extension version 0.0.4.

You must install this extension, if it is not already installed.

- Install ![vCardOOo logo][1] **[vCardOOo.oxt][20]** extension version 0.0.1.

Restart LibreOffice / OpenOffice after installation.

## Use:

In LibreOffice / OpenOffice go to File -> Wizards -> Address Data Source...:

![vCardOOo screenshot 1][21]

In step: 1. Address Book Type:
- select: Other external data source
- click on: Next(Button)

![vCardOOo screenshot 2][22]

In step: 2. Connection Settings:
- click on: Settings(Button)

![vCardOOo screenshot 3][23]

In Database type list:
- select: vCard Contacts
- click on: Next(Button)

![vCardOOo screenshot 4][24]

In General: Datasource Url:
- put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In General: User:
- put your username.

In General: Password:
- put your password.

Then:
- click on: Test connection (button)

![vCardOOo screenshot 5][25]

![vCardOOo screenshot 6][26]

![vCardOOo screenshot 7][27]

![vCardOOo screenshot 8][28]

![vCardOOo screenshot 9][29]

![vCardOOo screenshot 10][30]

![vCardOOo screenshot 11][31]

Have fun...

## Has been tested with:

* LibreOffice 7.2.5.2 - Ubuntu 20.04.3 LTS - LxQt 0.14.1

I encourage you in case of problem :-(  
to create an [issue][10]  
I will try to solve it ;-)

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your address book) stored in your Android phone.

With the [smtpMailerOOo][32] extension, it can be the data source for [mail merge][33] by email, to your correspondents contained in your phone.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver][34] responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource][35] singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator][36] thread to track remote changes on Nextcloud servers.
  - Create and cache a [User][37] Interface needed for:
    - Creating the connection to the underlying database.
    - Connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync][38] written in Java and using the [ez-vcard][39] library.

### What remains to be done for version 0.0.1:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...

[1]: <img/vCardOOo.png>
[2]: <https://prrvchr.github.io/vCardOOo/README_fr>
[3]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_en>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_en>
[5]: <https://prrvchr.github.io/vCardOOo#historical>
[6]: <https://prrvchr.github.io/>
[7]: <https://www.libreoffice.org/download/download/>
[8]: <https://www.openoffice.org/download/index.html>
[9]: <https://github.com/prrvchr/vCardOOo>
[10]: <https://github.com/prrvchr/vCardOOo/issues/new>
[11]: <http://hsqldb.org/>
[12]: <https://wiki.documentfoundation.org/Documentation/HowTo/Install_the_correct_JRE_-_LibreOffice_on_Windows_10>
[13]: <https://adoptium.net/releases.html?variant=openjdk11>
[14]: <https://bugs.documentfoundation.org/show_bug.cgi?id=139538>
[15]: <https://prrvchr.github.io/HsqlDBembeddedOOo/>
[16]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.png>
[17]: <https://github.com/prrvchr/OAuth2OOo/raw/master/OAuth2OOo.oxt>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.png>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/raw/master/source/jdbcDriverOOo/dist/jdbcDriverOOo.oxt>
[20]: <https://github.com/prrvchr/vCardOOo/raw/main/source/vCardOOo/dist/vCardOOo.oxt>
[21]: <img/vCardOOo-1.png>
[22]: <img/vCardOOo-2.png>
[23]: <img/vCardOOo-3.png>
[24]: <img/vCardOOo-4.png>
[25]: <img/vCardOOo-5.png>
[26]: <img/vCardOOo-6.png>
[27]: <img/vCardOOo-7.png>
[28]: <img/vCardOOo-8.png>
[29]: <img/vCardOOo-9.png>
[30]: <img/vCardOOo-10.png>
[31]: <img/vCardOOo-11.png>
[32]: <https://github.com/prrvchr/smtpMailerOOo/blob/master/source/smtpMailerOOo/dist/smtpMailerOOo.oxt>
[33]: <https://en.wikipedia.org/wiki/Mail_merge>
[34]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[35]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[36]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[37]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[38]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[39]: <https://github.com/mangstadt/ez-vcard>
