---
layout: default
title: vCardOOo documentation (English)
permalink: /
redirect_from:
  - /README
  - /README.html
---
<!--
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
-->
# [![vCardOOo logo][1]][2] Documentation

**Ce [document][3] en français.**

**The use of this software subjects you to our [Terms Of Use][4] and [Data Protection Policy][5].**

# version [1.4.1][6]

## Introduction:

**vCardOOo** is part of a [Suite][7] of [LibreOffice][8] ~~and/or [OpenOffice][9]~~ extensions allowing to offer you innovative services in these office suites.

This extension gives you access, in LibreOffice, to your contacts present on a [CardDAV server][10] (or vCard Extensions to WebDAV).  
It uses [RFC 6352][11] to synchronize your remote address book into a local HsqlDB 2.7.4 database.  
This extension is seen by LibreOffice as a [database driver][12] responding to the URL: `sdbc:address:vcard:*`.

Being free software I encourage you:
- To duplicate its [source code][13].
- To make changes, corrections, improvements.
- To open [issue][14] if needed.
- To [participate in the costs][15] of [CASA certification][16].

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

___

## Requirement:

The vCardOOo extension uses the OAuth2OOo extension to work.  
It must therefore meet the [requirement of the OAuth2OOo extension][17].

The vCardOOo extension uses the jdbcDriverOOo extension to work.  
It must therefore meet the [requirement of the jdbcDriverOOo extension][18].  
Additionally, vCardOOo requires the jdbcDriverOOo extension to be configured to provide `com.sun.star.sdb` as the API level, which is the default configuration.

___

## Installation:

It seems important that the file was not renamed when it was downloaded.  
If necessary, rename it before installing it.

- [![OAuth2OOo logo][19]][20] Install **[OAuth2OOo.oxt][21]** extension [![Version][22]][21]

  You must install this extension, if it is not already installed.

- [![jdbcDriverOOo logo][23]][24] Install **[jdbcDriverOOo.oxt][25]** extension [![Version][26]][25]

  You must install this extension, if it is not already installed.

- ![vCardOOo logo][27] Install **[vCardOOo.oxt][28]** extension [![Version][29]][28]

Restart LibreOffice after installation.  
**Be careful, restarting LibreOffice may not be enough.**
- **On Windows** to ensure that LibreOffice restarts correctly, use Windows Task Manager to verify that no LibreOffice services are visible after LibreOffice shuts down (and kill it if so).
- **Under Linux or macOS** you can also ensure that LibreOffice restarts correctly, by launching it from a terminal with the command `soffice` and using the key combination `Ctrl + C` if after stopping LibreOffice, the terminal is not active (no command prompt).

After this restart, you will be asked **to install Python packages containing binary files**. Please refer to the [Installing Python packages][30] section for more information.

After restarting LibreOffice, you can ensure that the extension and its driver are correctly installed by checking that the `io.github.prrvchr.vCardOOo.Driver` driver is listed in the **Connection Pool**, accessible via the menu: **Tools -> Options -> LibreOffice Base -> Connections**. It is not necessary to enable the connection pool.

If the driver is not listed, the reason for the driver failure can be found in the extension's logging. This log is accessible via the menu: **Tools -> Options -> LibreOffice Base -> CardDAV Contacts -> Logging Options**.  
The `vCardLog` logging must first be enabled and then LibreOffice restarted to get the error message in the log.

___

## Use:

In LibreOffice / OpenOffice go to: **File -> Wizards -> Address Data Source...**

![vCardOOo screenshot 1][31]

The **Address Book Datasource Wizard** open.

In step: **1.Address Book Type**:
- Select: **Other external data source**.
- Click button: **Next**.

![vCardOOo screenshot 2][32]

In step: **2.Connection Settings**:
- Click button: **Settings**.

![vCardOOo screenshot 3][33]

A new wizard opens. **Data source properties**.

In step: **1.Advanced Properties**.  
In Database type list:
- Select: **vCard Contacts**.
- click button: **Next**.

![vCardOOo screenshot 4][34]

In step: **2.Connection Settings**.  
In General: Enter the DBMS/driver-specific connection string here.
- Put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In User Authentication: User name:
- Put your username.
- Check the box: Password required

Then:
- Click button: **Test connection**.

![vCardOOo screenshot 5][35]

In Authentication required: Password:
- Put your password.

![vCardOOo screenshot 6][36]

Normally you should see: Connection Test: The connection was established successfully.

![vCardOOo screenshot 7][37]

If the connection has been established, you can complete this wizard with the **Finish** button.

![vCardOOo screenshot 8][38]

In step: **3.Table Selection**.  
If your data source has multiple tables, you will be asked to select the primary table.  
In this case select the table: **All my contacts**. If necessary and before any connection it is possible to rename the main table name in: **Tools -> Options -> Internet -> vCardOOo -> Main table name**.

In step: **4.Field Assignment**.  
If necessary it is possible to rename the names of the columns of the data source using the button: **Field Assignment**.  
Please continue this wizard with the button: **Next**.

![vCardOOo screenshot 9][39]

In step: **5.Data Source Title**.

You must create an odb file. To do this you must:
- **Uncheck the box**: Embed this address book definition in the current document.
- Named the odb file in the field: **Location**.

This odb file must also be made accessible. To do this you must:
- **Check the box**: Make this address book available to all modules in LibreOffice
- Named the address book in the field: **Address book name**.

![vCardOOo screenshot 10][40]

Have fun...

___

## How to build the extension:

Normally, the extension is created with Eclipse for Java and [LOEclipse][41]. To work around Eclipse, I modified LOEclipse to allow the extension to be created with Apache Ant.  
To create the vCardOOo extension with the help of Apache Ant, you need to:
- Install the [Java SDK][42] version 17 or higher.
- Install [Apache Ant][43] version 1.10.0 or higher.
- Install [LibreOffice and its SDK][44] version 7.x or higher.
- Clone the [vCardOOo][45] repository on GitHub into a folder.
- From this folder, move to the directory: `source/vCardOOo/`
- In this directory, edit the file: `build.properties` so that the `office.install.dir` and `sdk.dir` properties point to the folders where LibreOffice and its SDK were installed, respectively.
- Start the archive creation process using the command: `ant`
- You will find the generated archive in the subfolder: `dist/`

___

## Has been tested with:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 24.8.0.3 (x86_64) - Windows 10(x64) - Python version 3.9.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* **Does not work with OpenOffice on Windows** see [bug 128569][46]. Having no solution, I encourage you to install **LibreOffice**.

I encourage you in case of problem :confused:  
to create an [issue][14]  
I will try to solve it :smile:

___

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your vCard) stored on a Nextcloud server.

With the [eMailerOOo][47] extension, it can be the data source for [mail merge][48] by email, to your correspondents (your vCard) coming from the Nextcloud server.

It will give you access to an information system that only larges companies are able, today, to implement.

### [All changes are logged in the version History][49]

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo/fr/>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_en>
[5]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_en>
[6]: <https://prrvchr.github.io/vCardOOo#what-has-been-done-for-version-141>
[7]: <https://prrvchr.github.io/>
[8]: <https://www.libreoffice.org/download/download/>
[9]: <https://www.openoffice.org/download/index.html>
[10]: <https://en.wikipedia.org/wiki/CardDAV>
[11]: <https://www.rfc-editor.org/rfc/rfc6352.html>
[12]: <https://wiki.openoffice.org/wiki/Documentation/DevGuide/Database/Driver_Service>
[13]: <https://github.com/prrvchr/vCardOOo>
[14]: <https://github.com/prrvchr/vCardOOo/issues/new>
[15]: <https://github.com/sponsors/prrvchr>
[16]: <https://appdefensealliance.dev/casa>
[17]: <https://prrvchr.github.io/OAuth2OOo/#requirement>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/#requirement>
[19]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[20]: <https://prrvchr.github.io/OAuth2OOo/>
[21]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[22]: <https://img.shields.io/github/v/tag/prrvchr/OAuth2OOo?label=latest#right>
[23]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[24]: <https://prrvchr.github.io/jdbcDriverOOo/>
[25]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[26]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[27]: <https://prrvchr.github.io/vCardOOo/img/vCardOOo.svg#middle>
[28]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[29]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.4.1#right>
[30]: <./setup/>
[31]: <img/vCardOOo-1.png>
[32]: <img/vCardOOo-2.png>
[33]: <img/vCardOOo-3.png>
[34]: <img/vCardOOo-4.png>
[35]: <img/vCardOOo-5.png>
[36]: <img/vCardOOo-6.png>
[37]: <img/vCardOOo-7.png>
[38]: <img/vCardOOo-8.png>
[39]: <img/vCardOOo-9.png>
[40]: <img/vCardOOo-10.png>
[41]: <https://github.com/LibreOffice/loeclipse>
[42]: <https://adoptium.net/temurin/releases/?version=17&package=jdk>
[43]: <https://ant.apache.org/manual/install.html>
[44]: <https://downloadarchive.documentfoundation.org/libreoffice/old/7.6.7.2/>
[45]: <https://github.com/prrvchr/vCardOOo.git>
[46]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[47]: <https://prrvchr.github.io/eMailerOOo/>
[48]: <https://en.wikipedia.org/wiki/Mail_merge>
[49]: <https://prrvchr.github.io/vCardOOo/change/>
