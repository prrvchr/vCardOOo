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

# version [1.3.1][6]

## Introduction:

**vCardOOo** fait partie d'une [Suite][7] d'extensions [LibreOffice][8] ~~et/ou [OpenOffice][9]~~ permettant de vous offrir des services inovants dans ces suites bureautique.

Cette extension vous donne l'accès, dans LibreOffice, à vos contacts présent sur un [serveur CardDAV][10] (ou vCard Extensions to WebDAV).  
Elle utilise la [RFC 6352][11] pour synchroniser votre carnet d'adresses distant dans une base de données locale HsqlDB 2.7.4.  
Cette extension est vu par LibreOffice comme un [pilote de base de données][12] répondant à l'URL: `sdbc:address:vcard:*`.

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source][13].
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement][14] si nécessaire.

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

___

## Prérequis:

L'extension vCardOOo utilise l'extension OAuth2OOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension OAuth2OOo][15].

L'extension vCardOOo utilise l'extension jdbcDriverOOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension jdbcDriverOOo][16].  
De plus, vCardOOo nécessite que l'extension jdbcDriverOOo soit configurée pour fournir `com.sun.star.sdb` comme niveau d'API, qui est la configuration par défaut.

___

## Installation:

Il semble important que le fichier n'ait pas été renommé lors de son téléchargement.  
Si nécessaire, renommez-le avant de l'installer.

- [![OAuth2OOo logo][17]][18] Installer l'extension **[OAuth2OOo.oxt][19]** [![Version][20]][19]

    Vous devez installer cette extension, si elle n'est pas déjà installée.

- [![jdbcDriverOOo logo][21]][22] Installer l'extension **[jdbcDriverOOo.oxt][23]** [![Version][24]][23]

    Vous devez installer cette extension, si elle n'est pas déjà installée.

- ![vCardOOo logo][25] Installer l'extension **[vCardOOo.oxt][26]** [![Version][27]][26]

Redémarrez LibreOffice après l'installation.  
**Attention, redémarrer LibreOffice peut ne pas suffire.**
- **Sous Windows** pour vous assurer que LibreOffice redémarre correctement, utilisez le Gestionnaire de tâche de Windows pour vérifier qu'aucun service LibreOffice n'est visible après l'arrêt de LibreOffice (et tuez-le si ç'est le cas).
- **Sous Linux ou macOS** vous pouvez également vous assurer que LibreOffice redémarre correctement, en le lançant depuis un terminal avec la commande `soffice` et en utilisant la combinaison de touches `Ctrl + C` si après l'arrêt de LibreOffice, le terminal n'est pas actif (pas d'invité de commande).

Après avoir redémarré LibreOffice, vous pouvez vous assurer que l'extension et son pilote sont correctement installés en vérifiant que le pilote `io.github.prrvchr.vCardOOo.Driver` est répertorié dans le **Pool de Connexions**, accessible via le menu: **Outils -> Options -> LibreOffice Base -> Connexions**. Il n'est pas nécessaire d'activer le pool de connexions.

Si le pilote n'est pas répertorié, la raison de l'échec du chargement du pilote peut être trouvée dans la journalisation de l'extension. Cette journalisation est accessible via le menu: **Outils -> Options -> LibreOffice Base -> Contacts CardDAV -> Options de journalisation**.  
La journalisation `vCardLog` doit d'abord être activée, puis LibreOffice redémarré pour obtenir le message d'erreur dans le journal.

___

## Utilisation:

Dans LibreOffice / OpenOffice aller à: **Fichier -> Assistants -> Source de données des adresses...**

![vCardOOo screenshot 1][28]

L'**Assistant source de données du carnet d'adresses** s'ouvre.

À l'étape: **1.Type de carnet d'adresses**:
- Sélectionner: **Autre source de données externes**.
- Cliquez sur le bouton: **Suivant**.

![vCardOOo screenshot 2][29]

À l'étape: **2.Paramètres de Connexion**:
- Cliquez sur le bouton: **Paramètres**.

![vCardOOo screenshot 3][30]

Un nouvel assistant s'ouvre. **Propriétés de la source de données**.

A l'étape: **1.Propriétés avancées**.  
Dans Type de base de données:
- Sélectionner: **Contacts vCard**.
- Cliquez sur le bouton: **Suivant**.

![vCardOOo screenshot 4][31]

A l'étape: **2.Paramètres de connexion**.  
Dans Général: Entrer ici la chaîne de connexion spécifique au SGDB / pilote.
- Mettre l'url de votre instance Nextcloud (ie: nuage.distrilab.fr).

Dans Authentification de l'utilisateur: Nom d'utilisateur:
- Mettre votre nom d'utilisateur.
- Cochez la case: Mot de passe requis

Puis:
- Cliquez sur le bouton: **Tester la connexion**.

![vCardOOo screenshot 5][32]

Dans Authentification requise: Mot de passe:
- Mettre votre mot de passe.

![vCardOOo screenshot 6][33]

Normalement vous devez voir s'afficher: Test de connexion: Connexion établie.

![vCardOOo screenshot 7][34]

Si la connexion a été etablie, vous pouvez terminer cet assistant avec le bouton **Terminer**.

![vCardOOo screenshot 8][35]

A l'étape: **3.Sélection de table**.  
Si votre source de données comporte plusieurs tables, il vous sera demandé de sélectionner la table principale.  
Dans ce cas sélectionnez la table: **Tous mes contacts**. Si nécessaire et avant toute connexion il est possible de renommer le nom de la table principale dans: **Outils -> Options -> Internet -> vCardOOo -> Nom de la table principale**.

A l'étape: **4.Assignation de champ**.  
Si nécessaire il est possible de renommer les noms des colonnes de la source de données à l'aide du bouton: **Assignation de champ**.  
Veuillez poursuivre cet assistant par le bouton: **Suivant**.

![vCardOOo screenshot 9][36]

A l'étape: **5.Titre de la source de données**.

Il faut créer un fichier odb. Pour cela vous devez:
- **Décocher la case**: Intégrer cette définition du carnet d'adresses dans le document actuel.
- Nommer le fichier odb dans le champ: **Emplacement**.

Il faut également rendre accessible ce fichier odb. Pour cela vous devez:
- **Cocher la case**: Rendre ce carnet d'adresses accessible à tous les modules de LibreOffice
- Nommer le carnet d'adresses dans le champ: **Nom du carnet d'adresses**.

![vCardOOo screenshot 10][37]

Maintenant à vous d'en profiter...

___

## Comment créer l'extension:

Normalement, l'extension est créée avec Eclipse pour Java et [LOEclipse][38]. Pour contourner Eclipse, j'ai modifié LOEclipse afin de permettre la création de l'extension avec Apache Ant.  
Pour créer l'extension vCardOOo avec l'aide d'Apache Ant, vous devez:
- Installer le [SDK Java][39] version 17 ou supérieure.
- Installer [Apache Ant][40] version 1.10.0 ou supérieure.
- Installer [LibreOffice et son SDK][41] version 7.x ou supérieure.
- Cloner le dépôt [vCardOOo][42] sur GitHub dans un dossier.
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

* **Ne fonctionne pas avec OpenOffice sous Windows** voir [dysfonctionnement 128569][43]. N'ayant aucune solution, je vous encourrage d'installer **LibreOffice**.

Je vous encourage en cas de problème :confused:  
de créer un [dysfonctionnement][14]  
J'essaierai de le résoudre :smile:

___

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (vos vCard) stockées sur un serveur Nextcloud.

Avec l'extension [eMailerOOo][44], elle peut être la source de données pour des [publipostages][45] par courriel (email), à vos correspondants (vos vCard) provenant du serveur Nextcloud.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### Ce qui a été fait pour la version 0.0.1:

- Ecriture du service UNO [com.sun.star.sdbc.Driver][46] repondant à l'appel de l'url `sdbc:address:vcard:*`  
  La méthode `connect(url, info)` de ce pilote utilise le singleton [DataSource][47] pour renvoyer le service UNO `com.sun.star.sdbc.Connection`.

- Ce singleton DataSource est responsable de:

  - Lors de sa création, créer un thread [Replicator][48] pour suivre les modifications distantes sur les serveurs Nextcloud.
  - Créer et de mettre en cache une interface [User][49] nécessaire pour:
    - La création de la connexion à la base de données sous-jacente.
    - La connexion du Replicator au serveurs Nextcloud.
  - Démarrer le Replicator à chaque connexion à la base de données.

- Après avoir récupéré les modifications distantes, le Replicator utilise pour analyser le contenu des vCards un service UNO `com.sun.star.task.Job` [CardSync][50] écrit en Java et utilisant la bibliothèque [ez-vcard][51].

### Ce qui a été fait pour la version 1.0.1:

- L'absence ou l'obsolescence des extensions **OAuth2OOo** et/ou **jdbcDriverOOo** nécessaires au bon fonctionnement de **vCardOOo** affiche désormais un message d'erreur.

- Encore plein d'autres choses...

### Ce qui a été fait pour la version 1.0.2:

- Prise en charge de la version 1.2.0 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.0 ou ultérieure.

### Ce qui a été fait pour la version 1.0.3:

- Prise en charge de la version 1.2.1 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.1 ou ultérieure.

### Ce qui a été fait pour la version 1.1.0:

- Tous les paquets Python nécessaires à l'extension sont désormais enregistrés dans un fichier [requirements.txt][52] suivant la [PEP 508][53].
- Désormais si vous n'êtes pas sous Windows alors les paquets Python nécessaires à l'extension peuvent être facilement installés avec la commande:  
  `pip install requirements.txt`
- Modification de la section [Prérequis][54].

### Ce qui a été fait pour la version 1.1.1:

- Utilisation du package Python `dateutil` pour convertir les chaînes d'horodatage en UNO DateTime.
- De nombreuses autres corrections...

### Ce qui a été fait pour la version 1.1.2:

- Intégration d'un correctif pour contourner le [dysfonctionnement #159988][55].

### Ce qui a été fait pour la version 1.1.3:

- La création de la base de données, lors de la première connexion, utilise l'API UNO proposée par l'extension jdbcDriverOOo depuis la version 1.3.2. Cela permet d'enregistrer toutes les informations nécessaires à la création de la base de données dans 9 tables texte qui sont en fait [9 fichiers csv][56].
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.4 et 1.3.2 minimum.
- De nombreuses corrections.

### Ce qui a été fait pour la version 1.1.4:

- Mise à jour du paquet [Python python-dateutil][57] vers la version 2.9.0.post0.
- Mise à jour du paquet [Python decorator][58] vers la version 5.1.1.
- Mise à jour du paquet [Python packaging][59] vers la version 24.1.
- Mise à jour du paquet [Python setuptools][60] vers la version 72.1.0 afin de répondre à l'[alerte de sécurité Dependabot][61].
- Mise à jour du paquet [Python validators][62] vers la version 0.33.0.
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.6 et 1.4.2 minimum.

### Ce qui a été fait pour la version 1.1.5:

- Mise à jour du paquet [Python setuptools][60] vers la version 73.0.1.
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.7 et 1.4.5 minimum.
- Les modifications apportées aux options de l'extension, qui nécessitent un redémarrage de LibreOffice, entraîneront l'affichage d'un message.
- Support de LibreOffice version 24.8.x.

### Ce qui a été fait pour la version 1.1.6:

- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.8 et 1.4.6 minimum.
- Modification des options de l'extension accessibles via : **Outils -> Options... -> Internet -> vCardOOo** afin de respecter la nouvelle charte graphique.

### Ce qui a été fait pour la version 1.2.0:

- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.4.0 et 1.4.6 minimum.
- Il est possible de construire l'archive de l'extension (ie: le fichier oxt) avec l'utilitaire [Apache Ant][40] et le fichier script [build.xml][63].
- L'extension refusera de s'installer sous OpenOffice quelle que soit la version ou LibreOffice autre que 7.x ou supérieur.
- Ajout des fichiers binaires nécessaires aux bibliothèques Python pour fonctionner sous Linux et LibreOffice 24.8 (ie: Python 3.9).

### Ce qui a été fait pour la version 1.2.1:

- Mise à jour du paquet [Python packaging][59] vers la version 24.2.
- Mise à jour du paquet [Python setuptools][60] vers la version 75.8.0.
- Mise à jour du paquet [Python six][64] vers la version 1.17.0.
- Mise à jour du paquet [Python validators][62] vers la version 0.34.0.
- Support de Python version 3.13.

### Ce qui a été fait pour la version 1.3.0:

- Mise à jour du paquet [Python packaging][59] vers la version 25.0.
- Rétrogradage du paquet [Python setuptools][60] vers la version 75.3.2, afin d'assurer la prise en charge de Python 3.8.
- Déploiement de l'enregistrement passif permettant une installation beaucoup plus rapide des extensions et de différencier les services UNO enregistrés de ceux fournis par une implémentation Java ou Python. Cet enregistrement passif est assuré par l'extension [LOEclipse][38] via les [PR#152][65] et [PR#157][66].
- Modification de [LOEclipse][38] pour prendre en charge le nouveau format de fichier `rdb` produit par l'utilitaire de compilation `unoidl-write`. Les fichiers `idl` ont été mis à jour pour prendre en charge les deux outils de compilation disponibles: idlc et unoidl-write.
- Compilation de toutes les archives Java contenues dans l'extension sous forme de modules et avec **Java JDK version 17**.
- Il est désormais possible de créer le fichier oxt de l'extension vCardOOo uniquement avec Apache Ant et une copie du dépôt GitHub. La section [Comment créer l'extension][67] a été ajoutée à la documentation.
- Pour faciliter la construction sous Ant, les deux bibliothèques Java [ezvcard][68] et [vinnie][69] utilisées par vCardOOo ont été intégrées dans Eclipse aux côtés de vCardOOo et sont désormais compilées sous forme de module Java. Une [demande d'amélioration][70] a été faite pour trouver une solution plus simple si possible.
- Implémentation de [PEP 570][71] dans la [journalisation][72] pour prendre en charge les arguments multiples uniques.
- Toute erreur survenant lors du chargement du pilote sera consignée dans le journal de l'extension si la journalisation a été préalablement activé. Cela facilite l'identification des problèmes d'installation sous Windows.
- Pour garantir la création correcte de la base de données vCardOOo, il sera vérifié que l'extension jdbcDriverOOo a `com.sun.star.sdb` comme niveau d'API.
- Nécessite l'extension **jdbcDriverOOo en version 1.5.0 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.5.0 minimum**.

### Ce qui a été fait pour la version 1.3.1:

vCardOOo partage la bibliothèque Java `UnoHelper.jar` avec jdbcDriverOOo. La mise à jour de cette bibliothèque dans jdbcDriverOOo nécessite la même mise à jour dans vCardOOo.
- Nécessite l'extension **jdbcDriverOOo en version 1.5.4 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.5.1 minimum**.

### Que reste-t-il à faire pour la version 1.3.1:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_fr>
[5]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_fr>
[6]: <https://prrvchr.github.io/vCardOOo/README_fr#ce-qui-a-%C3%A9t%C3%A9-fait-pour-la-version-130>
[7]: <https://prrvchr.github.io/README_fr>
[8]: <https://fr.libreoffice.org/download/telecharger-libreoffice/>
[9]: <https://www.openoffice.org/fr/Telecharger/>
[10]: <https://fr.wikipedia.org/wiki/CardDAV>
[11]: <https://www.rfc-editor.org/rfc/rfc6352.html>
[12]: <https://wiki.openoffice.org/wiki/Documentation/DevGuide/Database/Driver_Service>
[13]: <https://github.com/prrvchr/vCardOOo>
[14]: <https://github.com/prrvchr/vCardOOo/issues/new>
[15]: <https://prrvchr.github.io/OAuth2OOo/README_fr#pr%C3%A9requis>
[16]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr#pr%C3%A9requis>
[17]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[18]: <https://prrvchr.github.io/OAuth2OOo/README_fr>
[19]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[20]: <https://img.shields.io/github/v/tag/prrvchr/OAuth2OOo?label=latest#right>
[21]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[22]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr>
[23]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[24]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[25]: <img/vCardOOo.svg#middle>
[26]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[27]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.3.0#right>
[28]: <img/vCardOOo-1_fr.png>
[29]: <img/vCardOOo-2_fr.png>
[30]: <img/vCardOOo-3_fr.png>
[31]: <img/vCardOOo-4_fr.png>
[32]: <img/vCardOOo-5_fr.png>
[33]: <img/vCardOOo-6_fr.png>
[34]: <img/vCardOOo-7_fr.png>
[35]: <img/vCardOOo-8_fr.png>
[36]: <img/vCardOOo-9_fr.png>
[37]: <img/vCardOOo-10_fr.png>
[38]: <https://github.com/LibreOffice/loeclipse>
[39]: <https://adoptium.net/temurin/releases/?version=17&package=jdk>
[40]: <https://ant.apache.org/manual/install.html>
[41]: <https://downloadarchive.documentfoundation.org/libreoffice/old/7.6.7.2/>
[42]: <https://github.com/prrvchr/vCardOOo.git>
[43]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[44]: <https://prrvchr.github.io/eMailerOOo/README_fr>
[45]: <https://en.wikipedia.org/wiki/Mail_merge>
[46]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[47]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[48]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[49]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[50]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[51]: <https://github.com/mangstadt/ez-vcard>
[52]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/requirements.txt>
[53]: <https://peps.python.org/pep-0508/>
[54]: <https://prrvchr.github.io/vCardOOo/README_fr#pr%C3%A9requis>
[55]: <https://bugs.documentfoundation.org/show_bug.cgi?id=159988>
[56]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vCardOOo/hsqldb>
[57]: <https://pypi.org/project/python-dateutil/>
[58]: <https://pypi.org/project/decorator/>
[59]: <https://pypi.org/project/packaging/>
[60]: <https://pypi.org/project/setuptools/>
[61]: <https://github.com/prrvchr/vCardOOo/security/dependabot/1>
[62]: <https://pypi.org/project/validators/>
[63]: <https://github.com/prrvchr/vCardOOo/blob/master/source/vCardOOo/build.xml>
[64]: <https://pypi.org/project/six/>
[65]: <https://github.com/LibreOffice/loeclipse/pull/152>
[66]: <https://github.com/LibreOffice/loeclipse/pull/157>
[67]: <https://prrvchr.github.io/vCardOOo/README_fr#comment-cr%C3%A9er-lextension>
[68]: <https://github.com/prrvchr/vCardOOo/tree/main/source/ezvcard>
[69]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vinnie>
[70]: <https://github.com/mangstadt/ez-vcard/issues/156>
[71]: <https://peps.python.org/pep-0570/>
[72]: <https://github.com/prrvchr/vCardOOo/blob/master/uno/lib/uno/logger/logwrapper.py#L109>
