
# Commande Basique 

## Commandes pour conteneurs

| Commande | Description |
| --- | --- |
| `docker-compose start` | Démarre un service présent |
| `docker-compose stop` | Stop un service |
| `docker [start/stop]` | Start/stop d'un container |
| `docker ps` | Liste les conteneurs en cours |
| `docker ps -a` | Affiche tous les docker présent sur le système |
| `docker-compose up (-d)` | Démarre un "Multi-Docker" (-d pour l'éxecution en arrière-plan) |
| `docker-compose down` | Stop un "Multi-conteneurs" |
| `docker rm <conteneur_name>` | Supprime un container |
| `docker rm -vf $(docker ps -aq)` | Supprime TOUS les containers |
| `docker build . -t <image-name> -f ./path/to/Dockerfile` | Build une image dans le contexte . |
| `docker run --it -d -rm --name=<conteneur_name> -p80:1234 -p<local_port>:<host_port> image:latest` | Run une image dans un conteneur |
| `docker exec -it <conteneur_name> /bin/bash` | Ouvre un shell dans un conteneur |
| `docker inspect <conteneur_name>` | Affiche des infos sur le container |
| `docker logs <conteneur_name>` | Affiche les logs d'un container |

## Commandes pour images 

| Commande | Description |
| --- | --- |
| `docker images -a` | Listes toutes les images (intermédiaires comprises) |
| `docker image prune -a` | Supprime toutes les images non utilisées et non associées à un conteneur |
| `docker image rm <image-name>` | Supprime une image  |
| `docker image inspect <image-name>` | Permet d'insepcter les layers de l'image |
| `docker rmi -f $(docker images -aq)`| Permet de supprimer toutes les images  |
