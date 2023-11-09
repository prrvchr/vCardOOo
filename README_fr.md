# Documentation

**This [document][1] in English.**

**L'utilisation de ce logiciel vous soumet à nos [Conditions d'utilisation][2] et à notre [Politique de protection des données][3]**.

# version [1.0.3][4]

## Introduction:

**vCardOOo** fait partie d'une [Suite][5] d'extensions [LibreOffice][6] ~~et/ou [OpenOffice][7]~~ permettant de vous offrir des services inovants dans ces suites bureautique.  
Cette extension vous donne l'accès, dans LibreOffice, à vos contacts présent sur un serveur CardDAV (ou vCard Extensions to WebDAV).

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source][8].
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement][9] si nécessaire.

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

___

## Prérequis:

Afin de profiter des dernières versions des bibliothèques Python utilisées dans vCardOOo, la version 2 de Python a été abandonnée au profit de **Python 3.8 minimum**.  
Cela signifie que **vCardOOo ne supporte plus OpenOffice et LibreOffice 6.x sous Windows depuis sa version 1.0.0**.
Je ne peux que vous conseiller **de migrer vers LibreOffice 7.x**.

vCardOOo utilise une base de données locale [HsqlDB][10] version 2.7.2.  
HsqlDB étant une base de données écrite en Java, son utilisation nécessite [l'installation et la configuration][11] dans LibreOffice / OpenOffice d'un **JRE version 11 ou ultérieure**.  
Je vous recommande [Adoptium][12] comme source d'installation de Java.

Si vous utilisez **LibreOffice Community sous Linux**, vous êtes sujet au [dysfonctionnement 139538][13]. Pour contourner le problème, veuillez **désinstaller les paquets** avec les commandes:
- `sudo apt remove libreoffice-sdbc-hsqldb` (pour désinstaller le paquet libreoffice-sdbc-hsqldb)
- `sudo apt remove libhsqldb1.8.0-java` (pour désinstaller le paquet libhsqldb1.8.0-java)

Si vous souhaitez quand même utiliser la fonctionnalité HsqlDB intégré fournie par LibreOffice, alors installez l'extension [HyperSQLOOo][14].  

___

## Installation:

Il semble important que le fichier n'ait pas été renommé lors de son téléchargement.  
Si nécessaire, renommez-le avant de l'installer.

- Installer l'extension ![OAuth2OOo logo][15] **[OAuth2OOo.oxt][16]** [![Version][17]][16]

Vous devez installer cette extension, si elle n'est pas déjà installée.

- Installer l'extension ![jdbcDriverOOo logo][18] **[jdbcDriverOOo.oxt][19]** [![Version][20]][19]

Vous devez installer cette extension, si elle n'est pas déjà installée.

- Installer l'extension ![vCardOOo logo][21] **[vCardOOo.oxt][22]** [![Version][23]][22]

Redémarrez LibreOffice / OpenOffice après l'installation.

___

## Utilisation:

Dans LibreOffice / OpenOffice aller à: Fichier -> Assistants -> Source de données des adresses...:

![vCardOOo screenshot 1][24]

À l'étape: 1. Type de carnet d'adresses:
- sélectionner: Autre source de données externes
- cliquez sur: Suivant (bouton)

![vCardOOo screenshot 2][25]

À l'étape: 2. Paramètres de Connexion:
- cliquez sur: Paramètres (bouton)

![vCardOOo screenshot 3][26]

Dans Type de base de données:
- sélectionner: Contacts vCard
- cliquez sur: Suivant (bouton)

![vCardOOo screenshot 4][27]

Dans Général: URL de la source de données:
- mettre l'url de votre instance Nextcloud (ie: nuage.distrilab.fr).

Dans Général: Utilisateur:
- mettre votre nom d'utilisateur.

Dans Général: Mot de passe:
- mettre votre mot de passe.

Puis:
- cliquez sur: Tester la connexion (bouton)

![vCardOOo screenshot 5][28]

![vCardOOo screenshot 6][29]

![vCardOOo screenshot 7][30]

![vCardOOo screenshot 8][31]

![vCardOOo screenshot 9][32]

![vCardOOo screenshot 10][33]

![vCardOOo screenshot 11][34]

Maintenant à vous d'en profiter...

___

## A été testé avec:

* LibreOffice 7.3.7.2 - Lubuntu 22.04 - Python version 3.10.12 - OpenJDK-11-JRE (amd64)

* LibreOffice 7.5.4.2(x86) - Windows 10 - Python version 3.8.16 - Adoptium JDK Hotspot 11.0.19 (under Lubuntu 22.04 / VirtualBox 6.1.38)

* LibreOffice 7.4.3.2(x64) - Windows 10(x64) - Python version 3.8.15  - Adoptium JDK Hotspot 11.0.17 (x64) (under Lubuntu 22.04 / VirtualBox 6.1.38)

* **Ne fonctionne pas avec OpenOffice sous Windows** voir [dysfonctionnement 128569][35]. N'ayant aucune solution, je vous encourrage d'installer **LibreOffice**.

Je vous encourage en cas de problème :confused:  
de créer un [dysfonctionnement][9]  
J'essaierai de le résoudre :smile:

___

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (votre carnet d'adresses) stockées dans votre téléphone Android.

Avec l'extension [eMailerOOo][36], elle peut être la source de données pour des [publipostages][37] par courriel (email), à vos correspondants contenus dans votre téléphone.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### Ce qui a été fait pour la version 0.0.1:

- Ecriture du service UNO [com.sun.star.sdbc.Driver][38] repondant à l'appel de l'url `sdbc:address:vcard:*`  
  La méthode `connect(url, info)` de ce pilote utilise le singleton [DataSource][39] pour renvoyer le service UNO `com.sun.star.sdbc.Connection`.

- Ce singleton DataSource est responsable de:

  - Lors de sa création, créer un thread [Replicator][40] pour suivre les modifications distantes sur les serveurs Nextcloud.
  - Créer et de mettre en cache une interface [User][41] nécessaire pour:
    - La création de la connexion à la base de données sous-jacente.
    - La connexion du Replicator au serveurs Nextcloud.
  - Démarrer le Replicator à chaque connexion à la base de données.

- Après avoir récupéré les modifications distantes, le Replicator utilise pour analyser le contenu des vCards un service UNO `com.sun.star.task.Job` [CardSync][42] écrit en Java et utilisant la bibliothèque [ez-vcard][43].

### Ce qui a été fait pour la version 1.0.1:

- L'absence ou l'obsolescence des extensions **OAuth2OOo** et/ou **jdbcDriverOOo** nécessaires au bon fonctionnement de **vCardOOo** affiche désormais un message d'erreur.

- Encore plein d'autres choses...

### Ce qui a été fait pour la version 1.0.2:

- Prise en charge de la version 1.2.0 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.0 ou ultérieure.

### Ce qui a été fait pour la version 1.0.3:

- Prise en charge de la version 1.2.1 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.1 ou ultérieure.

### Que reste-t-il à faire pour la version 1.0.3:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...

[1]: <https://prrvchr.github.io/vCardOOo>
[2]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_fr>
[3]: <https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_fr>
[4]: <https://prrvchr.github.io/vCardOOo#historical>
[5]: <https://prrvchr.github.io/README_fr>
[6]: <https://fr.libreoffice.org/download/telecharger-libreoffice/>
[7]: <https://www.openoffice.org/fr/Telecharger/>
[8]: <https://github.com/prrvchr/vCardOOo>
[9]: <https://github.com/prrvchr/vCardOOo/issues/new>
[10]: <http://hsqldb.org/>
[11]: <https://wiki.documentfoundation.org/Documentation/HowTo/Install_the_correct_JRE_-_LibreOffice_on_Windows_10/fr>
[12]: <https://adoptium.net/releases.html?variant=openjdk11>
[13]: <https://bugs.documentfoundation.org/show_bug.cgi?id=139538>
[14]: <https://prrvchr.github.io/HyperSQLOOo/README_fr>
[15]: <https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.svg#middle>
[16]: <https://github.com/prrvchr/OAuth2OOo/releases/latest/download/OAuth2OOo.oxt>
[17]: <https://img.shields.io/github/downloads/prrvchr/OAuth2OOo/latest/total?label=v1.2.1#right>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[20]: <https://img.shields.io/github/downloads/prrvchr/jdbcDriverOOo/latest/total?label=v1.0.5#right>
[21]: <img/vCardOOo.svg#middle>
[22]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/vCardOOo.oxt>
[23]: <https://img.shields.io/github/downloads/prrvchr/vCardOOo/latest/total?label=v1.0.3#right>
[24]: <img/vCardOOo-1_fr.png>
[25]: <img/vCardOOo-2_fr.png>
[26]: <img/vCardOOo-3_fr.png>
[27]: <img/vCardOOo-4_fr.png>
[28]: <img/vCardOOo-5_fr.png>
[29]: <img/vCardOOo-6_fr.png>
[30]: <img/vCardOOo-7_fr.png>
[31]: <img/vCardOOo-8_fr.png>
[32]: <img/vCardOOo-9_fr.png>
[33]: <img/vCardOOo-10_fr.png>
[34]: <img/vCardOOo-11_fr.png>
[35]: <https://bz.apache.org/ooo/show_bug.cgi?id=128569>
[36]: <https://prrvchr.github.io/eMailerOOo/README_fr>
[37]: <https://en.wikipedia.org/wiki/Mail_merge>
[38]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[39]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[40]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[41]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[42]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[43]: <https://github.com/mangstadt/ez-vcard>
