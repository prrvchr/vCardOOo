---
layout: default
title: vCardOOo history (English)
permalink: /change/
redirect_from:
  - /CHANGELOG
  - /CHANGELOG.html
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
# [![vCardOOo logo][1]][2] Historical

**Ce [document][3] en français.**

Regarding installation, configuration and use, please consult the **[documentation][4]**.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver][5] responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource][6] singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator][7] thread to track remote changes on Nextcloud servers.
  - Create and cache a [User][8] Interface needed for:
    - Creating the connection to the underlying database.
    - Connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync][9] written in Java and using the [ez-vcard][10] library.

### What has been done for version 1.0.1:

- The absence or obsolescence of the **OAuth2OOo** and/or **jdbcDriverOOo** extensions necessary for the proper functioning of **vCardOOo** now displays an error message.

- Many other things...

### What has been done for version 1.0.2:

- Support for version **1.2.0** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.0 or higher.

### What has been done for version 1.0.3:

- Support for version **1.2.1** of the **OAuth2OOo** extension. Previous versions will not work with **OAuth2OOo** extension 1.2.1 or higher.

### What has been done for version 1.1.0:

- All Python packages necessary for the extension are now recorded in a [requirements.txt][11] file following [PEP 508][12].
- Now if you are not on Windows then the Python packages necessary for the extension can be easily installed with the command:  
  `pip install requirements.txt`
- Modification of the [Requirement][13] section.

### What has been done for version 1.1.1:

- Using Python package `dateutil` to convert timestamp strings to UNO DateTime.
- Many other fixes...

### What has been done for version 1.1.2:

- Integration of a fix to workaround the [issue #159988][14].

### What has been done for version 1.1.3:

- The creation of the database, during the first connection, uses the UNO API offered by the jdbcDriverOOo extension since version 1.3.2. This makes it possible to record all the information necessary for creating the database in 9 text tables which are in fact [9 csv files][15].
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.4 and 1.3.2 respectively minimum.
- Many fixes.

### What has been done for version 1.1.4:

- Updated the [Python python-dateutil][16] package to version 2.9.0.post0.
- Updated the [Python decorator][17] package to version 5.1.1.
- Updated the [Python packaging][18] package to version 24.1.
- Updated the [Python setuptools][19] package to version 72.1.0 in order to respond to the [Dependabot security alert][20].
- Updated the [Python validators][21] package to version 0.33.0.
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.6 and 1.4.2 respectively minimum.

### What has been done for version 1.1.5:

- Updated the [Python setuptools][19] package to version 73.0.1.
- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.7 and 1.4.5 respectively minimum.
- Changes to extension options that require a restart of LibreOffice will result in a message being displayed.
- Support for LibreOffice version 24.8.x.

### What has been done for version 1.1.6:

- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.3.8 and 1.4.6 respectively minimum.
- Modification of the extension options accessible via: **Tools -> Options... -> Internet -> vCardOOo** in order to comply with the new graphic charter.

### What has been done for version 1.2.0:

- The extension will ask you to install the OAuth2OOo and jdbcDriverOOo extensions in versions 1.4.0 and 1.4.6 respectively minimum.
- It is possible to build the extension archive (ie: the oxt file) with the [Apache Ant][22] utility and the [build.xml][23] script file.
- The extension will refuse to install under OpenOffice regardless of version or LibreOffice other than 7.x or higher.
- Added binaries needed for Python libraries to work on Linux and LibreOffice 24.8 (ie: Python 3.9).

### What has been done for version 1.2.1:

- Updated the [Python packaging][18] package to version 24.2.
- Updated the [Python setuptools][19] package to version 75.8.0.
- Updated the [Python six][24] package to version 1.17.0.
- Updated the [Python validators][21] package to version 0.34.0.
- Support for Python version 3.13.

### What has been done for version 1.3.0:

- Updated the [Python packaging][18] package to version 25.0.
- Downgrade the [Python setuptools][19] package to version 75.3.2. to ensure support for Python 3.8.
- Passive registration deployment that allows for much faster installation of extensions and differentiation of registered UNO services from those provided by a Java or Python implementation. This passive registration is provided by the [LOEclipse][25] extension via [PR#152][26] and [PR#157][27].
- Modified [LOEclipse][25] to support the new `rdb` file format produced by the `unoidl-write` compilation utility. `idl` files have been updated to support both available compilation tools: idlc and unoidl-write.
- Compilation of all Java archives contained in the extension as modules and with **Java JDK version 17**.
- It is now possible to build the oxt file of the vCardOOo extension only with the help of Apache Ant and a copy of the GitHub repository. The [How to build the extension][28] section has been added to the documentation.
- To facilitate building under Ant, the two Java libraries [ezvcard][29] and [vinnie][30] used by vCardOOo have been integrated into Eclipse alongside vCardOOo and are now compiled as a Java module. An [enhancement request][31] has been made to find a simpler solution if possible.
- Implemented [PEP 570][32] in [logging][33] to support unique multiple arguments.
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

- All modal windows now open correctly in modal mode.
- Requires the **jdbcDriverOOo extension at least version 1.6.1**.
- Requires the **OAuth2OOo extension at least version 1.6.1**.

### What has been done for version 1.5.0:



### What remains to be done for version 1.5.0:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo/change/fr/>
[4]: <https://prrvchr.github.io/vCardOOo/>
[5]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[6]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[7]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[8]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[9]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[10]: <https://github.com/mangstadt/ez-vcard>
[11]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/requirements.txt>
[12]: <https://peps.python.org/pep-0508/>
[13]: <https://prrvchr.github.io/vCardOOo/#requirement>
[14]: <https://bugs.documentfoundation.org/show_bug.cgi?id=159988>
[15]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vCardOOo/hsqldb>
[16]: <https://pypi.org/project/python-dateutil/>
[17]: <https://pypi.org/project/decorator/>
[18]: <https://pypi.org/project/packaging/>
[19]: <https://pypi.org/project/setuptools/>
[20]: <https://github.com/prrvchr/vCardOOo/security/dependabot/1>
[21]: <https://pypi.org/project/validators/>
[22]: <https://ant.apache.org/manual/install.html>
[23]: <https://github.com/prrvchr/vCardOOo/blob/master/source/vCardOOo/build.xml>
[24]: <https://pypi.org/project/six/>
[25]: <https://github.com/LibreOffice/loeclipse>
[26]: <https://github.com/LibreOffice/loeclipse/pull/152>
[27]: <https://github.com/LibreOffice/loeclipse/pull/157>
[28]: <https://prrvchr.github.io/vCardOOo/#how-to-build-the-extension>
[29]: <https://github.com/prrvchr/vCardOOo/tree/main/source/ezvcard>
[30]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vinnie>
[31]: <https://github.com/mangstadt/ez-vcard/issues/156>
[32]: <https://peps.python.org/pep-0570/>
[33]: <https://github.com/prrvchr/vCardOOo/blob/master/uno/lib/uno/logger/logwrapper.py#L109>
