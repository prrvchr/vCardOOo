# ![vCardOOo logo](img/vCardOOo.png) vCardOOo

**Ce [document](https://prrvchr.github.io/vCardOOo/README_fr) en français.**

**The use of this software subjects you to our** [**Terms Of Use**](https://prrvchr.github.io/vCardOOo/vCardOOo/registration/TermsOfUse_en) **and** [**Data Protection Policy**](https://prrvchr.github.io/vCardOOo/vCardOOo/registration/PrivacyPolicy_en)

# version [0.0.6](https://prrvchr.github.io/vCardOOo#historical)

## Introduction:

**vCardOOo** is part of a [Suite](https://prrvchr.github.io/) of [LibreOffice](https://www.libreoffice.org/download/download/) and/or [OpenOffice](https://www.openoffice.org/download/index.html) extensions allowing to offer you innovative services in these office suites.  
This extension gives you access to your phone contacts in LibreOffice / OpenOffice (the contacts of your Android phone).

Being free software I encourage you:
- To duplicate its [source code](https://github.com/prrvchr/vCardOOo).
- To make changes, corrections, improvements.
- To open [issue](https://github.com/prrvchr/vCardOOo/issues/new) if needed.

In short, to participate in the development of this extension.  
Because it is together that we can make Free Software smarter.

## Requirement:

vCardOOo uses a local [HsqlDB](http://hsqldb.org/) database of version 2.5.1.  
The use of HsqlDB requires the installation and configuration within LibreOffice / OpenOffice of a **JRE version 1.8 minimum** (ie: Java version 8)  
I recommend [AdoptOpenJDK](https://adoptopenjdk.net/) as your Java installation source.

If you are using **LibreOffice on Linux**, then you are subject to [bug 139538](https://bugs.documentfoundation.org/show_bug.cgi?id=139538).  
To work around the problem, please uninstall the packages:
- libreoffice-sdbc-hsqldb
- libhsqldb1.8.0-java

If you still want to use the Embedded HsqlDB functionality provided by LibreOffice, then install the [HsqlDBembeddedOOo](https://prrvchr.github.io/HsqlDBembeddedOOo/) extension.  
OpenOffice and LibreOffice on Windows are not subject to this malfunction.

## Installation:

It seems important that the file was not renamed when it was downloaded.
If necessary, rename it before installing it.

- Install ![OAuth2OOo logo](https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.png) **[OAuth2OOo.oxt](https://github.com/prrvchr/OAuth2OOo/raw/master/OAuth2OOo.oxt)** extension version 0.0.5.

You must install this extension, if it is not already installed.

- Install ![HsqlDBDriverOOo logo](https://prrvchr.github.io/HsqlDBDriverOOo/img/HsqlDBDriverOOo.png) **[HsqlDBDriverOOo.oxt](https://github.com/prrvchr/HsqlDBDriverOOo/raw/master/HsqlDBDriverOOo.oxt)** extension version 0.0.4.

You must install this extension, if it is not already installed.

- Install ![vCardOOo logo](img/vCardOOo.png) **[vCardOOo.oxt](https://github.com/prrvchr/vCardOOo/raw/master/vCardOOo.oxt)** extension version 0.0.1.

Restart LibreOffice / OpenOffice after installation.

## Use:

In LibreOffice / OpenOffice go to File -> Wizards -> Address Data Source...:

![vCardOOo screenshot 1](img/vCardOOo-1.png)

In step: 1. Address Book Type:
- select: Other external data source
- click on: Next(Button)

![vCardOOo screenshot 2](img/vCardOOo-2.png)

In step: 2. Connection Settings:
- click on: Settings(Button)

![vCardOOo screenshot 3](img/vCardOOo-3.png)

In Database type list:
- select: Google Contacts
- click on: Next(Button)

![vCardOOo screenshot 4](img/vCardOOo-4.png)

In General: Datasource Url:
- put: your Google account (ie: your_account@gmail.com)

Then:
- click on: Test connection (button)

![vCardOOo screenshot 5](img/vCardOOo-5.png)

After authorizing the [OAuth2OOo](https://prrvchr.github.io/OAuth2OOo) application to access your Contacts, normally you should see: Connection Test: The connection was established successfully.

![vCardOOo screenshot 6](img/vCardOOo-6.png)

Have fun...

## Has been tested with:

* LibreOffice 6.4.4.2 - Ubuntu 20.04 -  LxQt 0.14.1

* LibreOffice 7.0.0.0.alpha1 - Ubuntu 20.04 -  LxQt 0.14.1

* OpenOffice 4.1.8 x86_64 - Ubuntu 20.04 - LxQt 0.14.1

* OpenOffice 4.2.0.Build:9820 x86_64 - Ubuntu 20.04 - LxQt 0.14.1

* LibreOffice 6.1.5.2 - Raspbian 10 buster - Raspberry Pi 4 Model B

* LibreOffice 6.4.4.2 (x64) - Windows 7 SP1

I encourage you in case of problem :-(  
to create an [issue](https://github.com/prrvchr/vCardOOo/issues/new)  
I will try to solve it ;-)

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your address book) stored in your Android phone.

With the [smtpMailerOOo](https://github.com/prrvchr/smtpMailerOOo/blob/master/smtpMailerOOo.oxt) extension, it can be the data source for [mail merge](https://en.wikipedia.org/wiki/Mail_merge) by email, to your correspondents contained in your phone.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Many other fix...

### What remains to be done for version 0.0.1:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...
