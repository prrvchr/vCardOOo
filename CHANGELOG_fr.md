---
layout: default
title: vCardOOo historique (Français)
permalink: /change/fr/
redirect_from:
  - /CHANGELOG_fr
  - /CHANGELOG_fr.html
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
# [![vCardOOo logo][1]][2] Historique

**This [document][3] in English.**

Concernant l'installation, la configuration et l'utilisation, veuillez consulter la **[documentation][4]**.

### Ce qui a été fait pour la version 0.0.1:

- Ecriture du service UNO [com.sun.star.sdbc.Driver][5] repondant à l'appel de l'url `sdbc:address:vcard:*`  
  La méthode `connect(url, info)` de ce pilote utilise le singleton [DataSource][6] pour renvoyer le service UNO `com.sun.star.sdbc.Connection`.

- Ce singleton DataSource est responsable de:

  - Lors de sa création, créer un thread [Replicator][7] pour suivre les modifications distantes sur les serveurs Nextcloud.
  - Créer et de mettre en cache une interface [User][8] nécessaire pour:
    - La création de la connexion à la base de données sous-jacente.
    - La connexion du Replicator au serveurs Nextcloud.
  - Démarrer le Replicator à chaque connexion à la base de données.

- Après avoir récupéré les modifications distantes, le Replicator utilise pour analyser le contenu des vCards un service UNO `com.sun.star.task.Job` [CardSync][9] écrit en Java et utilisant la bibliothèque [ez-vcard][10].

### Ce qui a été fait pour la version 1.0.1:

- L'absence ou l'obsolescence des extensions **OAuth2OOo** et/ou **jdbcDriverOOo** nécessaires au bon fonctionnement de **vCardOOo** affiche désormais un message d'erreur.

- Encore plein d'autres choses...

### Ce qui a été fait pour la version 1.0.2:

- Prise en charge de la version 1.2.0 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.0 ou ultérieure.

### Ce qui a été fait pour la version 1.0.3:

- Prise en charge de la version 1.2.1 de l'extension **OAuth2OOo**. Les versions précédentes ne fonctionneront pas avec l'extension **OAuth2OOo** 1.2.1 ou ultérieure.

### Ce qui a été fait pour la version 1.1.0:

- Tous les paquets Python nécessaires à l'extension sont désormais enregistrés dans un fichier [requirements.txt][11] suivant la [PEP 508][12].
- Désormais si vous n'êtes pas sous Windows alors les paquets Python nécessaires à l'extension peuvent être facilement installés avec la commande:  
  `pip install requirements.txt`
- Modification de la section [Prérequis][13].

### Ce qui a été fait pour la version 1.1.1:

- Utilisation du package Python `dateutil` pour convertir les chaînes d'horodatage en UNO DateTime.
- De nombreuses autres corrections...

### Ce qui a été fait pour la version 1.1.2:

- Intégration d'un correctif pour contourner le [dysfonctionnement #159988][14].

### Ce qui a été fait pour la version 1.1.3:

- La création de la base de données, lors de la première connexion, utilise l'API UNO proposée par l'extension jdbcDriverOOo depuis la version 1.3.2. Cela permet d'enregistrer toutes les informations nécessaires à la création de la base de données dans 9 tables texte qui sont en fait [9 fichiers csv][15].
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.4 et 1.3.2 minimum.
- De nombreuses corrections.

### Ce qui a été fait pour la version 1.1.4:

- Mise à jour du paquet [Python python-dateutil][16] vers la version 2.9.0.post0.
- Mise à jour du paquet [Python decorator][17] vers la version 5.1.1.
- Mise à jour du paquet [Python packaging][18] vers la version 24.1.
- Mise à jour du paquet [Python setuptools][19] vers la version 72.1.0 afin de répondre à l'[alerte de sécurité Dependabot][20].
- Mise à jour du paquet [Python validators][21] vers la version 0.33.0.
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.6 et 1.4.2 minimum.

### Ce qui a été fait pour la version 1.1.5:

- Mise à jour du paquet [Python setuptools][19] vers la version 73.0.1.
- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.7 et 1.4.5 minimum.
- Les modifications apportées aux options de l'extension, qui nécessitent un redémarrage de LibreOffice, entraîneront l'affichage d'un message.
- Support de LibreOffice version 24.8.x.

### Ce qui a été fait pour la version 1.1.6:

- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.3.8 et 1.4.6 minimum.
- Modification des options de l'extension accessibles via : **Outils -> Options... -> Internet -> vCardOOo** afin de respecter la nouvelle charte graphique.

### Ce qui a été fait pour la version 1.2.0:

- L'extension vous demandera d'installer les extensions OAuth2OOo et jdbcDriverOOo en version respectivement 1.4.0 et 1.4.6 minimum.
- Il est possible de construire l'archive de l'extension (ie: le fichier oxt) avec l'utilitaire [Apache Ant][22] et le fichier script [build.xml][23].
- L'extension refusera de s'installer sous OpenOffice quelle que soit la version ou LibreOffice autre que 7.x ou supérieur.
- Ajout des fichiers binaires nécessaires aux bibliothèques Python pour fonctionner sous Linux et LibreOffice 24.8 (ie: Python 3.9).

### Ce qui a été fait pour la version 1.2.1:

- Mise à jour du paquet [Python packaging][18] vers la version 24.2.
- Mise à jour du paquet [Python setuptools][19] vers la version 75.8.0.
- Mise à jour du paquet [Python six][24] vers la version 1.17.0.
- Mise à jour du paquet [Python validators][21] vers la version 0.34.0.
- Support de Python version 3.13.

### Ce qui a été fait pour la version 1.3.0:

- Mise à jour du paquet [Python packaging][18] vers la version 25.0.
- Rétrogradage du paquet [Python setuptools][19] vers la version 75.3.2, afin d'assurer la prise en charge de Python 3.8.
- Déploiement de l'enregistrement passif permettant une installation beaucoup plus rapide des extensions et de différencier les services UNO enregistrés de ceux fournis par une implémentation Java ou Python. Cet enregistrement passif est assuré par l'extension [LOEclipse][25] via les [PR#152][26] et [PR#157][27].
- Modification de [LOEclipse][25] pour prendre en charge le nouveau format de fichier `rdb` produit par l'utilitaire de compilation `unoidl-write`. Les fichiers `idl` ont été mis à jour pour prendre en charge les deux outils de compilation disponibles: idlc et unoidl-write.
- Compilation de toutes les archives Java contenues dans l'extension sous forme de modules et avec **Java JDK version 17**.
- Il est désormais possible de créer le fichier oxt de l'extension vCardOOo uniquement avec Apache Ant et une copie du dépôt GitHub. La section [Comment créer l'extension][28] a été ajoutée à la documentation.
- Pour faciliter la construction sous Ant, les deux bibliothèques Java [ezvcard][29] et [vinnie][30] utilisées par vCardOOo ont été intégrées dans Eclipse aux côtés de vCardOOo et sont désormais compilées sous forme de module Java. Une [demande d'amélioration][31] a été faite pour trouver une solution plus simple si possible.
- Implémentation de [PEP 570][32] dans la [journalisation][33] pour prendre en charge les arguments multiples uniques.
- Toute erreur survenant lors du chargement du pilote sera consignée dans le journal de l'extension si la journalisation a été préalablement activé. Cela facilite l'identification des problèmes d'installation sous Windows.
- Pour garantir la création correcte de la base de données vCardOOo, il sera vérifié que l'extension jdbcDriverOOo a `com.sun.star.sdb` comme niveau d'API.
- Nécessite l'extension **jdbcDriverOOo en version 1.5.0 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.5.0 minimum**.

### Ce qui a été fait pour la version 1.3.1:

vCardOOo partage la bibliothèque Java `UnoHelper.jar` avec jdbcDriverOOo. La mise à jour de cette bibliothèque dans jdbcDriverOOo nécessite la même mise à jour dans vCardOOo.
- Nécessite l'extension **jdbcDriverOOo en version 1.5.4 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.5.1 minimum**.

### Ce qui a été fait pour la version 1.3.2:

- Support de LibreOffice 25.2.x et 25.8.x sous Windows 64 bits.
- Nécessite l'extension **OAuth2OOo en version 1.5.2 minimum**.

### Ce qui a été fait pour la version 1.4.0:

- Si un mot de passe incorrect est fourni lors de la connexion à la source de données, il n'est plus nécessaire de redémarrer LibreOffice pour tenter de se connecter à nouveau.
- Si l'extension jdbcDriverOOo fonctionne sans l'instrumentation Java, un message d'avertissement s'affichera dans les options de l'extension.
- Nécessite l'extension **jdbcDriverOOo en version 1.6.0 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.6.0 minimum**.
- A été testé sous LibreOfficeDev 26.2.

### Ce qui a été fait pour la version 1.4.1:

- Toutes les fenêtres modales s'ouvrent désormais correctement en mode modal.
- Nécessite l'extension **jdbcDriverOOo en version 1.6.1 minimum**.
- Nécessite l'extension **OAuth2OOo en version 1.6.1 minimum**.

### Ce qui a été fait pour la version 1.5.0:



### Que reste-t-il à faire pour la version 1.5.0:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...

[1]: </img/contact.svg#collapse>
[2]: <https://prrvchr.github.io/vCardOOo/>
[3]: <https://prrvchr.github.io/vCardOOo/change/>
[4]: <https://prrvchr.github.io/vCardOOo/fr/>
[5]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/service/Driver.py>
[6]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/datasource.py>
[7]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/replicator.py>
[8]: <https://github.com/prrvchr/vCardOOo/blob/main/uno/lib/uno/card/card/user.py>
[9]: <https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java>
[10]: <https://github.com/mangstadt/ez-vcard>
[11]: <https://github.com/prrvchr/vCardOOo/releases/latest/download/requirements.txt>
[12]: <https://peps.python.org/pep-0508/>
[13]: <https://prrvchr.github.io/vCardOOo/fr/#pr%C3%A9requis>
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
[28]: <https://prrvchr.github.io/vCardOOo/fr/#comment-cr%C3%A9er-lextension>
[29]: <https://github.com/prrvchr/vCardOOo/tree/main/source/ezvcard>
[30]: <https://github.com/prrvchr/vCardOOo/tree/main/source/vinnie>
[31]: <https://github.com/mangstadt/ez-vcard/issues/156>
[32]: <https://peps.python.org/pep-0570/>
[33]: <https://github.com/prrvchr/vCardOOo/blob/master/uno/lib/uno/logger/logwrapper.py#L109>
