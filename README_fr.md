---
layout: default
title: vCardOOo documentation (Français)
permalink: /fr/
redirect_from:
  - /README_fr
  - /README_fr.html
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
# Documentation

**This [document][3] in English.**

**L'utilisation de ce logiciel vous soumet à nos [Conditions d'utilisation][4] et à notre [Politique de protection des données][5]**.

# version [1.4.1][6]

## Introduction:

**vCardOOo** fait partie d'une [Suite][7] d'extensions [LibreOffice][8] ~~et/ou [OpenOffice][9]~~ permettant de vous offrir des services inovants dans ces suites bureautique.

Cette extension vous donne l'accès, dans LibreOffice, à vos contacts présent sur un [serveur CardDAV][10] (ou vCard Extensions to WebDAV).  
Elle utilise la [RFC 6352][11] pour synchroniser votre carnet d'adresses distant dans une base de données locale HsqlDB 2.7.4.  
Cette extension est vu par LibreOffice comme un [pilote de base de données][12] répondant à l'URL: `sdbc:address:vcard:*`.

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source][13].
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement][14] si nécessaire.
- De [participer au frais][15] de la [certification CASA][16].

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

___

## Prérequis:

L'extension vCardOOo utilise l'extension OAuth2OOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension OAuth2OOo][17].

L'extension vCardOOo utilise l'extension jdbcDriverOOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension jdbcDriverOOo][18].  
De plus, vCardOOo nécessite que l'extension jdbcDriverOOo soit configurée pour fournir `com.sun.star.sdb` comme niveau d'API, qui est la configuration par défaut.

___

## Installation:

Il semble important que le fichier n'ait pas été renommé lors de son téléchargement.  
Si nécessaire, renommez-le avant de l'installer.

- [![OAuth2OOo logo][19]][20] Installer l'extension **[OAuth2OOo.oxt][21]** [![Version][22]][21]

    Vous devez installer cette extension, si elle n'est pas déjà installée.

- [![jdbcDriverOOo logo][23]][24] Installer l'extension **[jdbcDriverOOo.oxt][25]** [![Version][26]][25]

    Vous devez installer cette extension, si elle n'est pas déjà installée.

- ![vCardOOo logo][27] Installer l'extension **[vCardOOo.oxt][28]** [![Version][29]][28]

Redémarrez LibreOffice après l'installation.  
**Attention, redémarrer LibreOffice peut ne pas suffire.**
- **Sous Windows** pour vous assurer que LibreOffice redémarre correctement, utilisez le Gestionnaire de tâche de Windows pour vérifier qu'aucun service LibreOffice n'est visible après l'arrêt de LibreOffice (et tuez-le si ç'est le cas).
- **Sous Linux ou macOS** vous pouvez également vous assurer que LibreOffice redémarre correctement, en le lançant depuis un terminal avec la commande `soffice` et en utilisant la combinaison de touches `Ctrl + C` si après l'arrêt de LibreOffice, le terminal n'est pas actif (pas d'invité de commande).

Après ce redémarrage, il vous sera demandé **d'installer des paquets Python contenant des fichiers binaires**. Veuillez consulter la section [Installation de paquets Python][30] pour plus d'informations.

Après avoir redémarré LibreOffice, vous pouvez vous assurer que l'extension et son pilote sont correctement installés en vérifiant que le pilote `io.github.prrvchr.vCardOOo.Driver` est répertorié dans le **Pool de Connexions**, accessible via le menu: **Outils -> Options -> LibreOffice Base -> Connexions**. Il n'est pas nécessaire d'activer le pool de connexions.

Si le pilote n'est pas répertorié, la raison de l'échec du chargement du pilote peut être trouvée dans la journalisation de l'extension. Cette journalisation est accessible via le menu: **Outils -> Options -> LibreOffice Base -> Contacts CardDAV -> Options de journalisation**.  
La journalisation `vCardLog` doit d'abord être activée, puis LibreOffice redémarré pour obtenir le message d'erreur dans le journal.

___

## Utilisation:

Dans LibreOffice / OpenOffice aller à: **Fichier -> Assistants -> Source de données des adresses...**

![vCardOOo screenshot 1][31]

L'**Assistant source de données du carnet d'adresses** s'ouvre.

À l'étape: **1.Type de carnet d'adresses**:
- Sélectionner: **Autre source de données externes**.
- Cliquez sur le bouton: **Suivant**.

![vCardOOo screenshot 2][32]

À l'étape: **2.Paramètres de Connexion**:
- Cliquez sur le bouton: **Paramètres**.

![vCardOOo screenshot 3][33]

Un nouvel assistant s'ouvre. **Propriétés de la source de données**.

A l'étape: **1.Propriétés avancées**.  
Dans Type de base de données:
- Sélectionner: **Contacts vCard**.
- Cliquez sur le bouton: **Suivant**.

![vCardOOo screenshot 4][34]

A l'étape: **2.Paramètres de connexion**.  
Dans Général: Entrer ici la chaîne de connexion spécifique au SGDB / pilote.
- Mettre l'url de votre instance Nextcloud (ie: nuage.distrilab.fr).

Dans Authentification de l'utilisateur: Nom d'utilisateur:
- Mettre votre nom d'utilisateur.
- Cochez la case: Mot de passe requis

Puis:
- Cliquez sur le bouton: **Tester la connexion**.

![vCardOOo screenshot 5][35]

Dans Authentification requise: Mot de passe:
- Mettre votre mot de passe.

![vCardOOo screenshot 6][36]

Normalement vous devez voir s'afficher: Test de connexion: Connexion établie.

![vCardOOo screenshot 7][37]

Si la connexion a été etablie, vous pouvez terminer cet assistant avec le bouton **Terminer**.

![vCardOOo screenshot 8][38]

A l'étape: **3.Sélection de table**.  
Si votre source de données comporte plusieurs tables, il vous sera demandé de sélectionner la table principale.  
Dans ce cas sélectionnez la table: **Tous mes contacts**. Si nécessaire et avant toute connexion il est possible de renommer le nom de la table principale dans: **Outils -> Options -> Internet -> vCardOOo -> Nom de la table principale**.

A l'étape: **4.Assignation de champ**.  
Si nécessaire il est possible de renommer les noms des colonnes de la source de données à l'aide du bouton: **Assignation de champ**.  
Veuillez poursuivre cet assistant par le bouton: **Suivant**.

![vCardOOo screenshot 9][39]

A l'étape: **5.Titre de la source de données**.

Il faut créer un fichier odb. Pour cela vous devez:
- **Décocher la case**: Intégrer cette définition du carnet d'adresses dans le document actuel.
- Nommer le fichier odb dans le champ: **Emplacement**.

Il faut également rendre accessible ce fichier odb. Pour cela vous devez:
- **Cocher la case**: Rendre ce carnet d'adresses accessible à tous les modules de LibreOffice
- Nommer le carnet d'adresses dans le champ: **Nom du carnet d'adresses**.

![vCardOOo screenshot 10][40]

Maintenant à vous d'en profiter...

___

## Comment créer l'extension:

Normalement, l'extension est créée avec Eclipse pour Java et [LOEclipse][41]. Pour contourner Eclipse, j'ai modifié LOEclipse afin de permettre la création de l'extension avec Apache Ant.  
Pour créer l'extension vCardOOo avec l'aide d'Apache Ant, vous devez:
- Installer le [SDK Java][42] version 17 ou supérieure.
- Installer [Apache Ant][43] version 1.10.0 ou supérieure.
- Installer [LibreOffice et son SDK][44] version 7.x ou supérieure.
- Cloner le dépôt [vCardOOo][45] sur GitHub dans un dossier.
- Depuis ce dossier, accédez au répertoire: `source/vCardOOo/`
- Dans ce répertoire, modifiez le fichier `build.properties` afin que les propriétés `office.install.dir` et `sdk.dir` pointent vers les dossiers d'installation de LibreOffice et de son SDK, respectivement.
- Lancez la création de l'archive avec la commande: `ant`
- Vous trouverez l'archive générée dans le sous-dossier: `dist/`

___

## A été testé avec:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 24.8.0.3 (X86_64) - Windows 10(x64) - Python version 3.9.19 (sous Lubuntu 22.04 / VirtualBox 6.1.38)

* **Ne fonctionne pas avec OpenOffice sous Windows** voir [dysfonctionnement 128569][46]. N'ayant aucune solution, je vous encourrage d'installer **LibreOffice**.

Je vous encourage en cas de problème :confused:  
de créer un [dysfonctionnement][14]  
J'essaierai de le résoudre :smile:

___

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (vos vCard) stockées sur un serveur Nextcloud.

Avec l'extension [eMailerOOo][47], elle peut être la source de données pour des [publipostages][48] par courriel (email), à vos correspondants (vos vCard) provenant du serveur Nextcloud.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### [Toutes les changements sont consignées dans l'Historique des versions][49]

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_fr>
[5]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_fr>
[6]: <https://prrvchr.github.io/vCardOOo/README_fr#ce-qui-a-%C3%A9t%C3%A9-fait-pour-la-version-141>
[7]: <https://prrvchr.github.io/README_fr>
[8]: <https://fr.libreoffice.org/download/telecharger-libreoffice/>
[9]: <https://www.openoffice.org/fr/Telecharger/>
[10]: <https://fr.wikipedia.org/wiki/CardDAV>
[11]: <https://www.rfc-editor.org/rfc/rfc6352.html>
[12]: <https://wiki.openoffice.org/wiki/Documentation/DevGuide/Database/Driver_Service>
[13]: <https://github.com/prrvchr/vCardOOo>
[14]: <https://github.com/prrvchr/vCardOOo/issues/new>
[15]: <https://github.com/sponsors/prrvchr>
[16]: <https://appdefensealliance.dev/casa>
[17]: <https://prrvchr.github.io/OAuth2OOo/README_fr#pr%C3%A9requis>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr#pr%C3%A9requis>
[19]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[20]: <https://prrvchr.github.io/OAuth2OOo/README_fr>
[21]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[22]: <https://img.shields.io/github/v/tag/prrvchr/OAuth2OOo?label=latest#right>
[23]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[24]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr>
[25]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[26]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[27]: <img/vCardOOo.svg#middle>
[28]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[29]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.4.1#right>
[30]: <../setup/fr/>
[31]: <img/vCardOOo-1_fr.png>
[32]: <img/vCardOOo-2_fr.png>
[33]: <img/vCardOOo-3_fr.png>
[34]: <img/vCardOOo-4_fr.png>
[35]: <img/vCardOOo-5_fr.png>
[36]: <img/vCardOOo-6_fr.png>
[37]: <img/vCardOOo-7_fr.png>
[38]: <img/vCardOOo-8_fr.png>
[39]: <img/vCardOOo-9_fr.png>
[40]: <img/vCardOOo-10_fr.png>
[41]: <https://github.com/LibreOffice/loeclipse>
[42]: <https://adoptium.net/temurin/releases/?version=17&package=jdk>
[43]: <https://ant.apache.org/manual/install.html>
[44]: <https://downloadarchive.documentfoundation.org/libreoffice/old/7.6.7.2/>
[45]: <https://github.com/prrvchr/vCardOOo.git>
[46]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[47]: <https://prrvchr.github.io/eMailerOOo/README_fr>
[48]: <https://en.wikipedia.org/wiki/Mail_merge>
[49]: <https://prrvchr.github.io/vCardOOo/change/fr/>
