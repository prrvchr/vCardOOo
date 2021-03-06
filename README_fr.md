# ![vCardOOo logo](img/vCardOOo.png) vCardOOo

**This [document](https://prrvchr.github.io/vCardOOo) in English.**

**L'utilisation de ce logiciel vous soumet à nos** [**Conditions d'utilisation**](https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/TermsOfUse_fr) **et à notre** [**Politique de protection des données**](https://prrvchr.github.io/vCardOOo/source/vCardOOo/registration/PrivacyPolicy_fr)

# version [0.0.1](https://prrvchr.github.io/vCardOOo/README_fr#historique)

## Introduction:

**vCardOOo** fait partie d'une [Suite](https://prrvchr.github.io/README_fr) d'extensions [LibreOffice](https://fr.libreoffice.org/download/telecharger-libreoffice/) et/ou [OpenOffice](https://www.openoffice.org/fr/Telecharger/) permettant de vous offrir des services inovants dans ces suites bureautique.  
Cette extension vous donne l'acces à vos contacts téléphonique dans LibreOffice / OpenOffice (les contacts de votre téléphone Android).

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source](https://github.com/prrvchr/vCardOOo).
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement](https://github.com/prrvchr/vCardOOo/issues/new) si nécessaire.

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

## Prérequis:

vCardOOo utilise une base de données locale [HsqlDB](http://hsqldb.org/) version 2.5.1.  
HsqlDB étant une base de données écrite en Java, son utilisation nécessite [l'installation et la configuration](https://wiki.documentfoundation.org/Documentation/HowTo/Install_the_correct_JRE_-_LibreOffice_on_Windows_10/fr) dans LibreOffice / OpenOffice d'un **JRE version 11 ou ultérieure**.  
Je vous recommande [Adoptium](https://adoptium.net/releases.html?variant=openjdk11) comme source d'installation de Java.

Si vous utilisez **LibreOffice sous Linux**, alors vous êtes sujet au [dysfonctionnement 139538](https://bugs.documentfoundation.org/show_bug.cgi?id=139538).  
Pour contourner le problème, veuillez désinstaller les paquets:
- libreoffice-sdbc-hsqldb
- libhsqldb1.8.0-java

Si vous souhaitez quand même utiliser la fonctionnalité HsqlDB intégré fournie par LibreOffice, alors installez l'extension [HsqlDBembeddedOOo](https://prrvchr.github.io/HsqlDBembeddedOOo/README_fr).  
OpenOffice et LibreOffice sous Windows ne sont pas soumis à ce dysfonctionnement.

## Installation:

Il semble important que le fichier n'ait pas été renommé lors de son téléchargement.  
Si nécessaire, renommez-le avant de l'installer.

- Installer l'extension ![OAuth2OOo logo](https://prrvchr.github.io/OAuth2OOo/img/OAuth2OOo.png) **[OAuth2OOo.oxt](https://github.com/prrvchr/OAuth2OOo/raw/master/OAuth2OOo.oxt)** version 0.0.5.

Vous devez installer cette extension, si elle n'est pas déjà installée.

- Installer l'extension ![jdbcDriverOOo logo](https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.png) **[jdbcDriverOOo.oxt](https://github.com/prrvchr/jdbcDriverOOo/raw/master/source/jdbcDriverOOo/dist/jdbcDriverOOo.oxt)** version 0.0.4.

Vous devez installer cette extension, si elle n'est pas déjà installée.

- Installer l'extension ![vCardOOo logo](img/vCardOOo.png) **[vCardOOo.oxt](https://github.com/prrvchr/vCardOOo/raw/main/source/vCardOOo/dist/vCardOOo.oxt)** version 0.0.1.

Redémarrez LibreOffice / OpenOffice après l'installation.

## Utilisation:

Dans LibreOffice / OpenOffice aller à: Fichier -> Assistants -> Source de données des adresses...:

<!--- ![vCardOOo screenshot 1](img/vCardOOo-1_fr.png) --->

À l'étape: 1. Type de carnet d'adresses:
- sélectionner: Autre source de données externes
- cliquez sur: Suivant (bouton)

<!--- ![vCardOOo screenshot 2](img/vCardOOo-2_fr.png) --->

À l'étape: 2. Paramètres de Connexion:
- cliquez sur: Paramètres (bouton)

<!--- ![vCardOOo screenshot 3](img/vCardOOo-3_fr.png) --->

Dans Type de base de données:
- sélectionner: Contacts vCard
- cliquez sur: Suivant (bouton)

<!--- ![vCardOOo screenshot 4](img/vCardOOo-4_fr.png) --->

Dans Général: URL de la source de données:
- mettre l'url de votre instance Nextcloud (ie: nuage.distrilab.fr).

Dans Général: Utilisateur:
- mettre votre nom d'utilisateur.

Dans Général: Mot de passe:
- mettre votre mot de passe.

Puis:
- cliquez sur: Tester la connexion (bouton)

<!--- ![vCardOOo screenshot 5](img/vCardOOo-5_fr.png) --->

Maintenant à vous d'en profiter...

## A été testé avec:

* LibreOffice 7.2.5.2 - Ubuntu 20.04.3 LTS - LxQt 0.14.1

Je vous encourage en cas de problème :-(  
de créer un [dysfonctionnement](https://github.com/prrvchr/vCardOOo/issues/new)  
J'essaierai de le résoudre ;-)

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (votre carnet d'adresses) stockées dans votre téléphone Android.

Avec l'extension [smtpMailerOOo](https://prrvchr.github.io/smtpMailerOOo/README_fr), elle peut être la source de données pour des [publipostages](https://fr.wikipedia.org/wiki/Publipostage) par courriel (email), à vos correspondants contenus dans votre téléphone.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### Ce qui a été fait pour la version 0.0.1:

- Ecriture du service UNO [com.sun.star.sdbc.Driver](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/Driver.py) repondant à l'appel de l'url `sdbc:address:vcard:*`  
  La méthode `connect(url, info)` de ce pilote utilise le singleton [DataSource](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/datasource.py) pour renvoyer le service UNO `com.sun.star.sdbc.Connection`.

- Ce singleton DataSource est responsable de:

  - Lors de sa création, créer un thread [Replicator](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/replicator.py) pour suivre les modifications distantes sur les serveurs Nextcloud.
  - Créer et de mettre en cache une interface [User](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/pythonpath/vcard/user.py) nécessaire pour, la création de la connexion à la base de données sous-jacente et la connexion du Replicator au serveurs Nextcloud.
  - Démarrer le Replicator à chaque connexion à la base de données.

- Après avoir récupéré les modifications distantes, le Replicator utilise pour analyser le contenu des vCards un service UNO `com.sun.star.task.Job` [CardSync](https://github.com/prrvchr/vCardOOo/blob/main/source/vCardOOo/source/io/github/prrvchr/carddav/CardSync.java) écrit en Java et utilisant la bibliothèque [ez-vcard](https://github.com/mangstadt/ez-vcard).

### Que reste-t-il à faire pour la version 0.0.1:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...
