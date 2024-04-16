# YourTrace Docker

Ce dépôt contient le Dockerfile du projet YourTrace. 

- [Your Trace Docker](#your-trace-docker)
  * [Exigences](#exigences)
  * [Deploiement des conteneurs via script bash](#deploiement-des-conteneurs-via-script-bash)
  * [Flow d'execution du script](#flow-dexecution-du-script)
  * [Debug](#debug)

## Exigences

+ Docker-compose
+ Docker
+ Linux
+ Website folder
+ Git

Veuillez vous référer aux liens suivants pour l'installation de Docker sur votre distribution Linux :

| Distribution Linux | Lien d'installation Docker  |
| ------------- | ------------- |
| Ubuntu | https://docs.docker.com/engine/install/ubuntu/ |
| Debian | https://docs.docker.com/engine/install/debian/ |
| Fedora | https://docs.docker.com/engine/install/fedora/ |
| RHEL   | https://docs.docker.com/engine/install/rhel/ |
| CentOS | https://docs.docker.com/engine/install/centos/ |

Ajoutez votre utilisateur au groupe Docker :

```sudo usermod -aG docker ${USER}```

Pour appliquer la nouvelle appartenance au groupe : 

```su - ${USER}```

Avant de pouvoir clone, veuillez vous référer à la [documentation suivante](../Documentations/Before_use_git.md)  

Puis, clonez ce dépôt sur votre ordinateur en utilisant la commande suivante : 

```git clone https://gitlab.yourtrace.com/yourtrace/infra.git```

*Vous devez également avoir git clone le dossier infra et le dossier website dans le même dossier parent*

&rarr; /home/user/youtrace/*infra*  
&rarr; /home/user/youtrace/*website*


## Deploiement des conteneurs via script bash

**MERCI DE LIRE LE FLOW D'EXECUTION AVANT D'UTILISER LE SCRIPT.**

N'oubliez pas de rendre executable le script

`chmod +x install.sh`

Vous n'avez plus qu'à executer le script et vous laisser guider. 
Attention, le script ne permet pas l'utilisation avec `sudo`, merci de prendre les dispositions nécessaires. 

`./install.sh`

Si jamais vous souhaitez supprimer les conteneurs et le subnet YourTrace, utiliser la commande `docker-compose down` dans ce dossier. 


## Flow d'execution du script

### Étape 1: Vérifie les pré-requis
### Étape 2: Est-ce que le dossier Website est présent ?
-  Condition vraie?
       Vérifie si chaque branche est à jour, et propose de la mettre à jour à jour si elle ne l'est pas.
-  Condition fausse?
       Propose d'ajouter (git clone) le dossier depuis la branche main.       
### Étape 3: Copie le fichier d'environnement sample to .env
### Étape 4: Propose de choisir depuis quelle branche build l'image du Website. 
### Étape 5: Lancement du build des images des conteneurs
### Étape 6: Les conteneurs YourTrace existent déjà ? 
-  Condition vraie?
       Stop, Supprime puis recreate les conteneurs
-  Condition fausse?
       Créer les conteneurs 
### Étape Finale: Print des conteneurs running avec vérification du fonctionnement des 6 conteneurs. 

## Debug 

N'hésitez pas à prendre connaissance de notre [cheatsheet docker ](../Documentations/Aide_utilisation_Docker.md)
