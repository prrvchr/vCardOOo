# ![vCardOOo logo](img/vCardOOo.png) vCardOOo

**This [document](https://prrvchr.github.io/vCardOOo) in English.**

**L'utilisation de ce logiciel vous soumet à nos** [**Conditions d'utilisation**](https://prrvchr.github.io/vCardOOo/vCardOOo/registration/TermsOfUse_fr) **et à notre** [**Politique de protection des données**](https://prrvchr.github.io/vCardOOo/vCardOOo/registration/PrivacyPolicy_fr)

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
L'utilisation de HsqlDB nécessite l'installation et la configuration dans LibreOffice / OpenOffice d'un **JRE version 11 ou ultérieure**.  
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

- Installer l'extension ![HsqlDBDriverOOo logo](https://prrvchr.github.io/HsqlDBDriverOOo/img/HsqlDBDriverOOo.png) **[HsqlDBDriverOOo.oxt](https://github.com/prrvchr/HsqlDBDriverOOo/raw/master/HsqlDBDriverOOo.oxt)** version 0.0.4.

Vous devez installer cette extension, si elle n'est pas déjà installée.

- Installer l'extension ![vCardOOo logo](img/vCardOOo.png) **[vCardOOo.oxt](https://github.com/prrvchr/vCardOOo/raw/master/vCardOOo.oxt)** version 0.0.1.

Redémarrez LibreOffice / OpenOffice après l'installation.

## Utilisation:

Dans LibreOffice / OpenOffice aller à: Fichier -> Assistants -> Source de données des adresses...:

![vCardOOo screenshot 1](img/vCardOOo-1_fr.png)

À l'étape: 1. Type de carnet d'adresses:
- sélectionner: Autre source de données externes
- cliquez sur: Suivant (bouton)

![vCardOOo screenshot 2](img/vCardOOo-2_fr.png)

À l'étape: 2. Paramètres de Connexion:
- cliquez sur: Paramètres (bouton)

![vCardOOo screenshot 3](img/vCardOOo-3_fr.png)

Dans Type de base de données:
- sélectionner: Contacts vCard
- cliquez sur: Suivant (bouton)

![vCardOOo screenshot 4](img/vCardOOo-4_fr.png)

Dans Général: URL de la source de données:
- mettre l'url de votre instance vCard.

Dans Général: Utilisateur:
- mettre votre nom d'utilisateur.

Dans Général: Mot de passe:
- mettre votre mot de passe.

Puis:
- cliquez sur: Tester la connexion (bouton)

![vCardOOo screenshot 5](img/vCardOOo-5_fr.png)

Après avoir autorisé l'application [OAuth2OOo](https://prrvchr.github.io/OAuth2OOo/README_fr) à accéder à vos contacts, normalement vous devez voir s'afficher: Test de connexion: Connexion établie.

![vCardOOo screenshot 6](img/vCardOOo-6_fr.png)

Maintenant à vous d'en profiter...

## A été testé avec:

* LibreOffice 7.2.5.2 - Ubuntu 20.04 -  LXQt 0.14.1

Je vous encourage en cas de problème :-(  
de créer un [dysfonctionnement](https://github.com/prrvchr/vCardOOo/issues/new)  
J'essaierai de le résoudre ;-)

## Historique:

### Introduction:

Cette extension a été écrite afin de rendre utilisables dans un logiciel libre (LibreOffice ou OpenOffice) vos données personnelles (votre carnet d'adresses) stockées dans votre téléphone Android.

Avec l'extension [smtpMailerOOo](https://github.com/prrvchr/smtpMailerOOo/blob/master/smtpMailerOOo.oxt), elle peut être la source de données pour des [publipostages](https://fr.wikipedia.org/wiki/Publipostage) par courriel (email), à vos correspondants contenus dans votre téléphone.

Elle vous donnera accès à un système d'information que seules les grandes entreprises sont capables, aujourd'hui, de mettre en œuvre.

### Ce qui a été fait pour la version 0.0.1:

- Beaucoup d'autres correctifs...

### Que reste-t-il à faire pour la version 0.0.1:

- Rendre le carnet d'adresses modifiable localement avec la réplication des modifications.

- Ajouter de nouvelles langues pour l'internationalisation...

- Tout ce qui est bienvenu...
