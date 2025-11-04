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

After restarting LibreOffice, you can ensure that the extension and its driver are correctly installed by checking that the `io.github.prrvchr.vCardOOo.Driver` driver is listed in the **Connection Pool**, accessible via the menu: **Tools -> Options -> LibreOffice Base -> Connections**. It is not necessary to enable the connection pool.

If the driver is not listed, the reason for the driver failure can be found in the extension's logging. This log is accessible via the menu: **Tools -> Options -> LibreOffice Base -> CardDAV Contacts -> Logging Options**.  
The `vCardLog` logging must first be enabled and then LibreOffice restarted to get the error message in the log.

___

## Use:

In LibreOffice / OpenOffice go to: **File -> Wizards -> Address Data Source...**

![vCardOOo screenshot 1][30]

The **Address Book Datasource Wizard** open.

In step: **1.Address Book Type**:
- Select: **Other external data source**.
- Click button: **Next**.

![vCardOOo screenshot 2][31]

In step: **2.Connection Settings**:
- Click button: **Settings**.

![vCardOOo screenshot 3][32]

A new wizard opens. **Data source properties**.

In step: **1.Advanced Properties**.  
In Database type list:
- Select: **vCard Contacts**.
- click button: **Next**.

![vCardOOo screenshot 4][33]

In step: **2.Connection Settings**.  
In General: Enter the DBMS/driver-specific connection string here.
- Put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In User Authentication: User name:
- Put your username.
- Check the box: Password required

Then:
- Click button: **Test connection**.

![vCardOOo screenshot 5][34]

In Authentication required: Password:
- Put your password.

![vCardOOo screenshot 6][35]

Normally you should see: Connection Test: The connection was established successfully.

![vCardOOo screenshot 7][36]

If the connection has been established, you can complete this wizard with the **Finish** button.

![vCardOOo screenshot 8][37]

In step: **3.Table Selection**.  
If your data source has multiple tables, you will be asked to select the primary table.  
In this case select the table: **All my contacts**. If necessary and before any connection it is possible to rename the main table name in: **Tools -> Options -> Internet -> vCardOOo -> Main table name**.

In step: **4.Field Assignment**.  
If necessary it is possible to rename the names of the columns of the data source using the button: **Field Assignment**.  
Please continue this wizard with the button: **Next**.

![vCardOOo screenshot 9][38]

In step: **5.Data Source Title**.

You must create an odb file. To do this you must:
- **Uncheck the box**: Embed this address book definition in the current document.
- Named the odb file in the field: **Location**.

This odb file must also be made accessible. To do this you must:
- **Check the box**: Make this address book available to all modules in LibreOffice
- Named the address book in the field: **Address book name**.

![vCardOOo screenshot 10][39]

Have fun...

___

## How to build the extension:

Normally, the extension is created with Eclipse for Java and [LOEclipse][40]. To work around Eclipse, I modified LOEclipse to allow the extension to be created with Apache Ant.  
To create the vCardOOo extension with the help of Apache Ant, you need to:
- Install the [Java SDK][41] version 17 or higher.
- Install [Apache Ant][42] version 1.10.0 or higher.
- Install [LibreOffice and its SDK][43] version 7.x or higher.
- Clone the [vCardOOo][44] repository on GitHub into a folder.
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

* **Does not work with OpenOffice on Windows** see [bug 128569][45]. Having no solution, I encourage you to install **LibreOffice**.

I encourage you in case of problem :confused:  
to create an [issue][14]  
I will try to solve it :smile:

___

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your vCard) stored on a Nextcloud server.

With the [eMailerOOo][46] extension, it can be the data source for [mail merge][47] by email, to your correspondents (your vCard) coming from the Nextcloud server.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver][48] responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource][49] singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator][50] thread to track remote changes on Nextcloud servers.
  - Create and cache a [User][51] Interface needed for:
    - Creating the connection to the underlying database.
    - Connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync][52] written in Java and using the [ez-vcard][53] library.

### What has been done for version 1.0.1:

- The absence or obsolescence of the **OAuth2OOo** and/or **jdbcDriverOOo** extensions necessary for the proper functioning of **vCardOOo** now displays an error message.

- Many other things...

### What has been done for version 1.0.2:

- Support for version **1.2.0** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.0 or higher.

### What has been done for version 1.0.3:

- Support for version **1.2.1** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.1 or higher.

### What has been done for version 1.1.0:

- All Python packages necessary for the extension are now recorded in a [requirements.txt][54] file following [PEP 508][55].
- Now if you are not on Windows then the Python packages necessary for the extension can be easily installed with the command:  
  `pip install requirements.txt`
- Modification of the [Requirement][56] section.

### What has been done for version 1.1.1:

- Using Python package `dateutil` to convert timestamp strings to UNO DateTime.
- Many other fixes...

### What has been done for version 1.1.2:

- Integration of a fix to workaround the [issue #159988][57].

### What has been done for version 1.1.3:

- The creation of the database, during the first connection, uses the UNO API offered by the jdbcDriverOOo extension since version 1.3.2. This makes it possible to record all the information necessary for creating the database in 9 text tables which are in fact [9 csv files][58].
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.4 and 1.3.2 respectively minimum.
- Many fixes.

### What has been done for version 1.1.4:

- Updated the [Python python-dateutil][59] package to version 2.9.0.post0.
- Updated the [Python decorator][60] package to version 5.1.1.
- Updated the [Python packaging][61] package to version 24.1.
- Updated the [Python setuptools][62] package to version 72.1.0 in order to respond to the [Dependabot security alert][63].
- Updated the [Python validators][64] package to version 0.33.0.
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.6 and 1.4.2 respectively minimum.

### What has been done for version 1.1.5:

- Updated the [Python setuptools][62] package to version 73.0.1.
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.7 and 1.4.5 respectively minimum.
- Changes to extension options that require a restart of LibreOffice will result in a message being displayed.
- Support for LibreOffice version 24.8.x.

### What has been done for version 1.1.6:

- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.8 and 1.4.6 respectively minimum.
- Modification of the extension options accessible via: **Tools -> Options... -> Internet -> vCardOOo** in order to comply with the new graphic charter.

### What has been done for version 1.2.0:

- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.4.0 and 1.4.6 respectively minimum.
- It is possible to build the extension archive (ie: the oxt file) with the [Apache Ant][42] utility and the [build.xml][65] script file.
- The extension will refuse to install under OpenOffice regardless of version or LibreOffice other than 7.x or higher.
- Added binaries needed for Python libraries to work on Linux and LibreOffice 24.8 (ie: Python 3.9).

### What has been done for version 1.2.1:

- Updated the [Python packaging][61] package to version 24.2.
- Updated the [Python setuptools][62] package to version 75.8.0.
- Updated the [Python six][66] package to version 1.17.0.
- Updated the [Python validators][64] package to version 0.34.0.
- Support for Python version 3.13.

### What has been done for version 1.3.0:

- Updated the [Python packaging][61] package to version 25.0.
- Downgrade the [Python setuptools][62] package to version 75.3.2. to ensure support for Python 3.8.
- Passive registration deployment that allows for much faster installation of extensions and differentiation of registered UNO services from those provided by a Java or Python implementation. This passive registration is provided by the [LOEclipse][40] extension via [PR#152][67] and [PR#157][68].
- Modified [LOEclipse][40] to support the new `rdb` file format produced by the `unoidl-write` compilation utility. `idl` files have been updated to support both available compilation tools: idlc and unoidl-write.
- Compilation of all Java archives contained in the extension as modules and with **Java JDK version 17**.
- It is now possible to build the oxt file of the vCardOOo extension only with the help of Apache Ant and a copy of the GitHub repository. The [How to build the extension][69] section has been added to the documentation.
- To facilitate building under Ant, the two Java libraries [ezvcard][70] and [vinnie][71] used by vCardOOo have been integrated into Eclipse alongside vCardOOo and are now compiled as a Java module. An [enhancement request][72] has been made to find a simpler solution if possible.
- Implemented [PEP 570][73] in [logging][74] to support unique multiple arguments.
- Any errors occurring while loading the driver will be logged in the extension's log if logging has been previously enabled. This makes it easier to identify installation problems on Windows.
- To ensure the correct creation of the vCardOOo database, it will be checked that the jdbcDriverOOo extension has `com.sun.star.sdb` as API level.
- Requires the **jdbcDriverOOo extension at least version 1.5.0**.
- Requires the **OAuth2OOo extension at least version 1.5.0**.

### What has been done for version 1.3.1:

vCardOOo shares the Java library `UnoHelper.jar` with jdbcDriverOOo. Updating this library in jdbcDriverOOo requires the same update in vCardOOo.
- Requires the **jdbcDriverOOo extension at least version 1.5.4**.
- Requires the **OAuth2OOo extension at least version 1.5.1**.

### What has been done for version 1.3.2:

- Support for LibreOffice 25.2.x and 25.8.x on Windows 64-bit.
- Requires the **OAuth2OOo extension at least version 1.5.2**.

### What has been done for version 1.4.0:

- If an incorrect password is provided when connecting to the data source, it is no longer necessary to restart LibreOffice to attempt to connect again.
- If the jdbcDriverOOo extension works without Java instrumentation, a warning message will be displayed in the extension options.
- Requires the **jdbcDriverOOo extension at least version 1.6.0**.
- Requires the **OAuth2OOo extension at least version 1.6.0**.
- Has been tested under LibreOfficeDev 26.2.

### What has been done for version 1.4.1:

- Requires the **jdbcDriverOOo extension at least version 1.6.1**.
- Requires the **OAuth2OOo extension at least version 1.6.1**.

### What remains to be done for version 1.4.1:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo/README_fr>
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
[27]: <img/vCardOOo.svg#middle>
[28]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[29]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.4.1#right>
[30]: <img/vCardOOo-1.png>
[31]: <img/vCardOOo-2.png>
[32]: <img/vCardOOo-3.png>
[33]: <img/vCardOOo-4.png>
[34]: <img/vCardOOo-5.png>
[35]: <img/vCardOOo-6.png>
[36]: <img/vCardOOo-7.png>
[37]: <img/vCardOOo-8.png>
[38]: <img/vCardOOo-9.png>
[39]: <img/vCardOOo-10.png>
[40]: <https://github.com/LibreOffice/loeclipse>
[41]: <https://adoptium.net/temurin/releases/?version=17&package=jdk>
[42]: <https://ant.apache.org/manual/install.html>
[43]: <https://downloadarchive.documentfoundation.org/libreoffice/old/7.6.7.2/>
[44]: <https://github.com/prrvchr/vCardOOo.git>
[45]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[46]: <https://prrvchr.github.io/eMailerOOo/>
[47]: <https://en.wikipedia.org/wiki/Mail_merge>
[48]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[49]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[50]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[51]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[52]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[53]: <https://github.com/mangstadt/ez-vcard>
[54]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/requirements.txt>
[55]: <https://peps.python.org/pep-0508/>
[56]: <https://prrvchr.github.io/vCardOOo/#requirement>
[57]: <https://bugs.documentfoundation.org/show_bug.cgi?id=159988>
[58]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vCardOOo/hsqldb>
[59]: <https://pypi.org/project/python-dateutil/>
[60]: <https://pypi.org/project/decorator/>
[61]: <https://pypi.org/project/packaging/>
[62]: <https://pypi.org/project/setuptools/>
[63]: <https://github.com/prrvchr/vCardOOo/security/dependabot/1>
[64]: <https://pypi.org/project/validators/>
[65]: <https://github.com/prrvchr/vCardOOo/blob/master/source/vCardOOo/build.xml>
[66]: <https://pypi.org/project/six/>
[67]: <https://github.com/LibreOffice/loeclipse/pull/152>
[68]: <https://github.com/LibreOffice/loeclipse/pull/157>
[69]: <https://prrvchr.github.io/vCardOOo/#how-to-build-the-extension>
[70]: <https://github.com/prrvchr/vCardOOo/tree/main/source/ezvcard>
[71]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vinnie>
[72]: <https://github.com/mangstadt/ez-vcard/issues/156>
[73]: <https://peps.python.org/pep-0570/>
[74]: <https://github.com/prrvchr/vCardOOo/blob/master/uno/lib/uno/logger/logwrapper.py#L109>
