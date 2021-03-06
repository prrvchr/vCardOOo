# ![vCardOOo logo](img/vCardOOo.png) vCardOOo

**Ce [document](https://prrvchr.github.io/vCardOOo/README_fr) en français.**

**The use of this software subjects you to our** [**Terms Of Use**](https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_en) **and** [**Data Protection Policy**](https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_en)

# version [0.0.1](https://prrvchr.github.io/vCardOOo#historical)

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

vCardOOo uses a local [HsqlDB](http://hsqldb.org/) database version 2.5.1.  
HsqlDB being a database written in Java, its use requires the [installation and configuration](https://wiki.documentfoundation.org/Documentation/HowTo/Install_the_correct_JRE_-_LibreOffice_on_Windows_10) in LibreOffice / OpenOffice of a **JRE version 11 or later**.  
I recommend [Adoptium](https://adoptium.net/releases.html?variant=openjdk11) as your Java installation source.

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

- Install ![jdbcDriverOOo logo](https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.png) **[jdbcDriverOOo.oxt](https://github.com/prrvchr/jdbcDriverOOo/raw/master/source/jdbcDriverOOo/dist/jdbcDriverOOo.oxt)** extension version 0.0.4.

You must install this extension, if it is not already installed.

- Install ![vCardOOo logo](img/vCardOOo.png) **[vCardOOo.oxt](https://github.com/prrvchr/vCardOOo/raw/main/source/vCardOOo/dist/vCardOOo.oxt)** extension version 0.0.1.

Restart LibreOffice / OpenOffice after installation.

## Use:

In LibreOffice / OpenOffice go to File -> Wizards -> Address Data Source...:

<!--- ![vCardOOo screenshot 1](img/vCardOOo-1.png) --->

In step: 1. Address Book Type:
- select: Other external data source
- click on: Next(Button)

<!--- ![vCardOOo screenshot 2](img/vCardOOo-2.png) --->

In step: 2. Connection Settings:
- click on: Settings(Button)

<!--- ![vCardOOo screenshot 3](img/vCardOOo-3.png) --->

In Database type list:
- select: vCard Contacts
- click on: Next(Button)

<!--- ![vCardOOo screenshot 4](img/vCardOOo-4.png) --->

In General: Datasource Url:
- put the url of your Nextcloud instance (ie: nuage.distrilab.fr).

In General: User:
- put your username.

In General: Password:
- put your password.

Then:
- click on: Test connection (button)

<!--- ![vCardOOo screenshot 5](img/vCardOOo-5.png) --->

Have fun...

## Has been tested with:

* LibreOffice 7.2.5.2 - Ubuntu 20.04.3 LTS - LxQt 0.14.1

I encourage you in case of problem :-(  
to create an [issue](https://github.com/prrvchr/vCardOOo/issues/new)  
I will try to solve it ;-)

## Historical:

### Introduction:

This extension was written in order to make usable in free software (LibreOffice or OpenOffice) your personal data (your address book) stored in your Android phone.

With the [smtpMailerOOo](https://prrvchr.github.io/smtpMailerOOo) extension, it can be the data source for [mail merge](https://en.wikipedia.org/wiki/Mail_merge) by email, to your correspondents contained in your phone.

It will give you access to an information system that only larges companies are able, today, to implement.

### What has been done for version 0.0.1:

- Writing of the UNO service [com.sun.star.sdbc.Driver](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/Driver.py) responding to the call from the url `sdbc:address:vcard:*`  
  The `connect(url, info)` method of this Driver use the [DataSource](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/datasource.py) singleton to return the UNO service `com.sun.star.sdbc.Connection`.

- This DataSource singleton is responsible for:

  - When created, create a [Replicator](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/replicator.py) thread to track remote changes on Nextcloud servers.
  - Create and cache a [User](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/user.py) Interface needed for, creating the connection to the underlying database and connect the Replicator to Nextcloud servers.
  - Start the Replicator each time you connect to the database.

-  After retrieving the remote modifications, the Replicator uses to analyze the content of the vCards a UNO `com.sun.star.task.Job` service [CardSync](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java) written in Java and using the [ez-vcard](https://github.com/mangstadt/ez-vcard) library.

### What remains to be done for version 0.0.1:

- Make the address book locally editable with replication of changes.

- Add new languages for internationalization...

- Anything welcome...
