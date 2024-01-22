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
# Documentation

**This [document][3] in English.**

**L'utilisation de ce logiciel vous soumet à nos [Conditions d'utilisation][4] et à notre [Politique de protection des données][5]**.

# version [1.1.1][6]

## Introduction:

**vCardOOo** fait partie d'une [Suite][7] d'extensions [LibreOffice][8] ~~et/ou [OpenOffice][9]~~ permettant de vous offrir des services inovants dans ces suites bureautique.  
Cette extension vous donne l'accès, dans LibreOffice, à vos contacts présent sur un serveur CardDAV (ou vCard Extensions to WebDAV).

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source][10].
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement][11] si nécessaire.

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

___

## Prérequis:

L'extension vCardOOo utilise l'extension OAuth2OOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension OAuth2OOo][12].

L'extension vCardOOo utilise l'extension jdbcDriverOOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension jdbcDriverOOo][13].

**Sous Linux et macOS les paquets Python** utilisés par l'extension, peuvent s'il sont déja installé provenir du système et donc, **peuvent ne pas être à jour**.  
Afin de s'assurer que vos paquets Python sont à jour il est recommandé d'utiliser l'option **Info système** dans les Options de l'extension accessible par:  
**Outils -> Options -> Internet -> vCardOOo -> Voir journal -> Info système**  
Si des paquets obsolètes apparaissent, vous pouvez les mettre à jour avec la commande:  
`pip install --upgrade <package-name>`

Pour plus d'information voir: [Ce qui a été fait pour la version 1.1.0][14].

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

**Sous Windows, redémarrer LibreOffice peut ne pas suffire.**  
Pour vous assurer que LibreOffice redémarre correctement, utilisez le Gestionnaire de tâche de Windows pour vérifier qu'aucun service LibreOffice n'est visible après l'arrêt de LibreOffice.

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

## A été testé avec:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* **Ne fonctionne pas avec OpenOffice sous Windows** voir [dysfonctionnement 128569][38]. N'ayant aucune solution, je vous encourrage d'installer **LibreOffice**.

Je vous encourage en cas de problème :confused:  
de créer un [dysfonctionnement][11]  
J'essaierai de le résoudre :smile:

___

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (vos vCard) stockées sur un serveur Nextcloud.

Avec l'extension [eMailerOOo][39], elle peut être la source de données pour des [publipostages][40] par courriel (email), à vos correspondants (vos vCard) provenant du serveur Nextcloud.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### Ce qui a été fait pour la version 0.0.1:

- Ecriture du service UNO [com.sun.star.sdbc.Driver][41] repondant à l'appel de l'url `sdbc:address:vcard:*`  
  La méthode `connect(url, info)` de ce pilote utilise le singleton [DataSource][42] pour renvoyer le service UNO `com.sun.star.sdbc.Connection`.

- Ce singleton DataSource est responsable de:

  - Lors de sa création, créer un thread [Replicator][43] pour suivre les modifications distantes sur les serveurs Nextcloud.
  - Créer et de mettre en cache une interface [User][44] nécessaire pour:
    - La création de la connexion à la base de données sous-jacente.
    - La connexion du Replicator au serveurs Nextcloud.
  - Démarrer le Replicator à chaque connexion à la base de données.

- Après avoir récupéré les modifications distantes, le Replicator utilise pour analyser le contenu des vCards un service UNO `com.sun.star.task.Job` [CardSync][45] écrit en Java et utilisant la bibliothèque [ez-vcard][46].

### Ce qui a été fait pour la version 1.0.1:

- L'absence ou l'obsolescence des extensions **OAuth2OOo** et/ou **jdbcDriverOOo** nécessaires au bon fonctionnement de **vCardOOo** affiche désormais un message d'erreur.

- Encore plein d'autres choses...

### Ce qui a été fait pour la version 1.0.2:

- Prise en charge de la version 1.2.0 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.0 ou ultérieure.

### Ce qui a été fait pour la version 1.0.3:

- Prise en charge de la version 1.2.1 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.1 ou ultérieure.

### Ce qui a été fait pour la version 1.1.0:

- Tous les paquets Python nécessaires à l'extension sont désormais enregistrés dans un fichier [requirements.txt][47] suivant la [PEP 508][48].
- Désormais si vous n'êtes pas sous Windows alors les paquets Python nécessaires à l'extension peuvent être facilement installés avec la commande:  
  `pip install requirements.txt`
- Modification de la section [Prérequis][49].

### Ce qui a été fait pour la version 1.1.1:

- Utilisation du package Python `dateutil` pour convertir les chaînes d'horodatage en UNO DateTime.
- De nombreuses autres corrections...

### Que reste-t-il à faire pour la version 1.1.1:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo>
[4]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_fr>
[5]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_fr>
[6]: <https://prrvchr.github.io/vCardOOo/README_fr#historique>
[7]: <https://prrvchr.github.io/README_fr>
[8]: <https://fr.libreoffice.org/download/telecharger-libreoffice/>
[9]: <https://www.openoffice.org/fr/Telecharger/>
[10]: <https://github.com/prrvchr/vCardOOo>
[11]: <https://github.com/prrvchr/vCardOOo/issues/new>
[12]: <https://prrvchr.github.io/OAuth2OOo/README_fr#pr%C3%A9requis>
[13]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr#pr%C3%A9requis>
[14]: <https://prrvchr.github.io/vCardOOo/README_fr#ce-qui-a-%C3%A9t%C3%A9-fait-pour-la-version-110>
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
[27]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.1.1#right>
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
[38]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[39]: <https://prrvchr.github.io/eMailerOOo/README_fr>
[40]: <https://en.wikipedia.org/wiki/Mail_merge>
[41]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[42]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[43]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[44]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[45]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[46]: <https://github.com/mangstadt/ez-vcard>
[47]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vCardOOo/requirements.txt>
[48]: <https://peps.python.org/pep-0508/>
[49]: <https://prrvchr.github.io/vCardOOo/README_fr#pr%C3%A9requis>
