# Your Trace Docker

Ce dépôt contient le Dockerfile du projet YourTrace, permettant le déploiement instantané d'un serveur LAMP.

- [Your Trace Docker](#your-trace-docker)
  * [Exigences](#exigences)
  * [Installation et exécution](#installation-et-ex-cution)
    + [Installation](#installation)
    + [Exécution](#ex-cution)
    + [Mise à jour de la partie Web](#mise---jour-de-la-partie-web)
  * [Cheat SHEET](#cheat-sheet)
    + [Commande Basique](#commande-basique)
    + [Debug](#debug)


## Exigences

+  Composer 2.2 >
+  Docker 23.0.1 >

## Installation et exécution


### Installation

Clonez ce dépôt sur votre ordinateur en utilisant la commande suivante :

```git clone https://gitlab.yourtrace.com/yourtrace/infra.git```

Veuillez vous référer aux liens suivants pour l'installation de Docker sur votre distribution Linux :

| Distribution Linux | Lien d'installation Docker  |
| ------------- | ------------- |
| Ubuntu | https://docs.docker.com/engine/install/ubuntu/ |
| Debian | https://docs.docker.com/engine/install/debian/ |
| Fedora | https://docs.docker.com/engine/install/fedora/ |
| RHEL | https://docs.docker.com/engine/install/rhel/ |
| CentOS | https://docs.docker.com/engine/install/centos/ |

### Exécution

1. Une fois que le dépôt a été cloné à l'emplacement de votre choix, exécutez les commandes suivantes pour démarrer le serveur :

```
cd infra/YourTrace_Docker
docker compose build
```

2. Une fois que Docker a installé toutes ses dépendances, exécutez le conteneur Docker avec la commande suivante :


```
docker compose up -d
```

Note : Il y a un système de vérification de l'état du conteneur mariadb, assurez-vous que son état est bien **UP** et **Healthy**.

3. Une fois que les 3 conteneurs sont UP, vous devrez vous connecter en shell sur le conteneur Web afin créer un fichier **/var/www/html/.env** ainsi que de télécharger les dépendances via **composer** en utilisant la commande suivante :


Exemple fichier .env: 
```
APP_NAME=YourTrace
APP_PORT=8100
APP_PORT_UNSECURE=8101
PHPADMIN_PORT=8102
DB_PORT=33016

MYSQL_ROOT_PASS=docker
MYSQL_ROOT_PASSWORD=docker
MYSQL_USER=docker
MYSQL_PASS=docker
MYSQL_DB=database

```

Installation des dépendances via **composer**: 

```
docker compose exec webserver bash
composer install
```


### Mise à jour de la partie Web

Pour mettre à jour la partie Web, remplacez le dossier `infra/YourTrace_Docker/website` par le nouveau dossier, puis réexécutez les commandes de la section **Exécution**.


## Cheat SHEET 

### Commande Basique

| Commande | Description |
| --- | --- |
| `docker-compose start` | Démarre un service présent |
| `docker-compose stop` | Stop un service |
| `docker-compose ps` | Liste les "Multi-Docker" en cours |
| `docker-compose up (-d)` | Démarre un "Multi-Docker" (-d pour l'éxecution en arrière-plan) |
| `docker-compose down` | Stop un "Multi-Docker" |
| `docker ps -a` | Affiche tous les docker présent sur le système |
| `docker rm CONTAINER` | Supprime un container |
| `docker [start/stop]` | Start/stop d'un container |

### Debug

| Commande | Description |
| --- | --- |
| `docker inspect CONTAINER` | Affiche des infos sur le container |
| `docker logs CONTAINER` | Affiche les logs d'un container |