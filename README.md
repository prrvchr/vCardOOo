<!--
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
-->
# [![vCardOOo logo][1]][2] Documentation

**Ce [document][3] en français.**

**The use of this software subjects you to our [Terms Of Use][4] and [Data Protection Policy][5].**

# version [1.1.1][6]

## Introduction:

**vCardOOo** is part of a [Suite][7] of [LibreOffice][8] ~~and/or [OpenOffice][9]~~ extensions allowing to offer you innovative services in these office suites.  
This extension gives you access, in LibreOffice, to your contacts present on a CardDAV server (or vCard Extensions to WebDAV).

Being free software I encourage you:
- To duplicate its [source code][10].
- To make changes, corrections, improvements.
- To open [issue][11] if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

___

## Requirement:

The vCardOOo extension uses the OAuth2OOo extension to work.  
It must therefore meet the [requirement of the OAuth2OOo extension][12].

The vCardOOo extension uses the jdbcDriverOOo extension to work.  
It must therefore meet the [requirement of the jdbcDriverOOo extension][13].

**On Linux and macOS the Python packages** used by the extension, if already installed, may come from the system and therefore **may not be up to date**.  
To ensure that your Python packages are up to date it is recommended to use the **System Info** option in the extension Options accessible by:  
**Tools -> Options -> Internet -> vCardOOo -> View log -> System Info**  
If outdated packages appear, you can update them with the command:  
`pip install --upgrade <package-name>`

For more information see: [What has been done for version 1.1.0][14].

___

## Installation:

It seems important that the file was not renamed when it was downloaded.
If necessary, rename it before installing it.

- [![OAuth2OOo logo][17]][18] Install **[OAuth2OOo.oxt][19]** extension [![Version][20]][19]

    You must install this extension, if it is not already installed.

- [![jdbcDriverOOo logo][21]][22] Install **[jdbcDriverOOo.oxt][23]** extension [![Version][24]][23]

    You must install this extension, if it is not already installed.

- ![vCardOOo logo][25] Install **[vCardOOo.oxt][26]** extension [![Version][27]][26]

Restart LibreOffice after installation.

**On Windows, restarting LibreOffice may not be enough.**  
To ensure that LibreOffice restarts correctly, use the Windows Task Manager to verify that no LibreOffice services are visible after LibreOffice is shut down.

___

## Use:

In LibreOffice / OpenOffice go to: **File -> Wizards -> Address Data Source...**

![vCardOOo screenshot 1][28]

The **Address Book Datasource Wizard** open.

In step: **1.Address Book Type**:
- Select: **Other external data source**.
- Click button: **Next**.

![vCardOOo screenshot 2][29]

In step: **2.Connection Settings**:
- Click button: **Settings**.

![vCardOOo screenshot 3][30]

A new wizard opens. **Data source properties**.

In step: **1.Advanced Properties**.  
In Database type list:
- Select: **vCard Contacts**.
- click button: **Next**.

![vCardOOo screenshot 4][31]

In step: **2.Connection Settings**.  
In General: Enter the DBMS/driver-specific connection string here.
- Put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In User Authentication: User name:
- Put your username.
- Check the box: Password required

Then:
- Click button: **Test connection**.

![vCardOOo screenshot 5][32]

In Authentication required: Password:
- Put your password.

![vCardOOo screenshot 6][33]

Normally you should see: Connection Test: The connection was established successfully.

![vCardOOo screenshot 7][34]

If the connection has been established, you can complete this wizard with the **Finish** button.

![vCardOOo screenshot 8][35]

In step: **3.Table Selection**.  
If your data source has multiple tables, you will be asked to select the primary table.  
In this case select the table: **All my contacts**. If necessary and before any connection it is possible to rename the main table name in: **Tools -> Options -> Internet -> vCardOOo -> Main table name**.

In step: **4.Field Assignment**.  
If necessary it is possible to rename the names of the columns of the data source using the button: **Field Assignment**.  
Please continue this wizard with the button: **Next**.

![vCardOOo screenshot 9][36]

In step: **5.Data Source Title**.

You must create an odb file. To do this you must:
- **Uncheck the box**: Embed this address book definition in the current document.
- Named the odb file in the field: **Location**.

This odb file must also be made accessible. To do this you must:
- **Check the box**: Make this address book available to all modules in LibreOffice
- Named the address book in the field: **Address book name**.

![vCardOOo screenshot 10][37]

Have fun...

___

## Has been tested with:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* **Does not work with OpenOffice on Windows** see [bug 128569][38]. Having no solution, I encourage you to install **LibreOffice**.

I encourage you in case of problem :confused:  
to create an [issue][11]  
I will try to solve it :smile:

___

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your vCard) stored on a Nextcloud server.

With the [eMailerOOo][39] extension, it can be the data source for [mail merge][40] by email, to your correspondents (your vCard) coming from the Nextcloud server.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver][41] responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource][42] singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator][43] thread to track remote changes on Nextcloud servers.
  - Create and cache a [User][44] Interface needed for:
    - Creating the connection to the underlying database.
    - Connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync][45] written in Java and using the [ez-vcard][46] library.

### What has been done for version 1.0.1:

- The absence or obsolescence of the **OAuth2OOo** and/or **jdbcDriverOOo** extensions necessary for the proper functioning of **vCardOOo** now displays an error message.

- Many other things...

### What has been done for version 1.0.2:

- Support for version **1.2.0** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.0 or higher.

### What has been done for version 1.0.3:

- Support for version **1.2.1** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.1 or higher.

### What has been done for version 1.1.0:

- All Python packages necessary for the extension are now recorded in a [requirements.txt][47] file following [PEP 508][48].
- Now if you are not on Windows then the Python packages necessary for the extension can be easily installed with the command:  
  `pip install requirements.txt`
- Modification of the [Requirement][49] section.

### What has been done for version 1.1.0:

- Using Python package `dateutil` to convert timestamp strings to UNO DateTime.
- Many other fixes...

### What remains to be done for version 1.1.0:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo/README_fr>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_en>
[5]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_en>
[6]: <https://prrvchr.github.io/vCardOOo#historical>
[7]: <https://prrvchr.github.io/>
[8]: <https://www.libreoffice.org/download/download/>
[9]: <https://www.openoffice.org/download/index.html>
[10]: <https://github.com/prrvchr/vCardOOo>
[11]: <https://github.com/prrvchr/vCardOOo/issues/new>
[12]: <https://prrvchr.github.io/OAuth2OOo/#requirement>
[13]: <https://prrvchr.github.io/jdbcDriverOOo/#requirement>
[14]: <https://prrvchr.github.io/vCardOOo/#what-has-been-done-for-version-110>
[17]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[18]: <https://prrvchr.github.io/OAuth2OOo/>
[19]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[20]: <https://img.shields.io/github/v/tag/prrvchr/OAuth2OOo?label=latest#right>
[21]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[22]: <https://prrvchr.github.io/jdbcDriverOOo/>
[23]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[24]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[25]: <img/vCardOOo.svg#middle>
[26]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[27]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.1.1#right>
[28]: <img/vCardOOo-1.png>
[29]: <img/vCardOOo-2.png>
[30]: <img/vCardOOo-3.png>
[31]: <img/vCardOOo-4.png>
[32]: <img/vCardOOo-5.png>
[33]: <img/vCardOOo-6.png>
[34]: <img/vCardOOo-7.png>
[35]: <img/vCardOOo-8.png>
[36]: <img/vCardOOo-9.png>
[37]: <img/vCardOOo-10.png>
[38]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[39]: <https://prrvchr.github.io/eMailerOOo/>
[40]: <https://en.wikipedia.org/wiki/Mail_merge>
[41]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[42]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[43]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[44]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[45]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[46]: <https://github.com/mangstadt/ez-vcard>
[47]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vCardOOo/requirements.txt>
[48]: <https://peps.python.org/pep-0508/>
[49]: <https://prrvchr.github.io/vCardOOo/#requirement>
