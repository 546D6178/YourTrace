# Repo officiel de la web app Your Trace

**Liens utiles :**
- [Documentation de Symfony]('https://symfony.com/doc/current/index.html')

## Environnement :
- PHP 8.3*
- Composer 
- Apache2
- MYSQL (ou MariaDB, faut voir comment ça se passe)

## Installation :

1. Installer Symfony-cli (reccommandé)
  https://symfony.com/download

2. Cloner le repo:
```
git clone git@github.com:Guerisan/yourtrace.git
```

3. Se rendre dans le dossier de projet
```
cd yourtrace
```

4. Installer les dépendances :
```
composer install
```

5. Créer une base de données mysql (le service mysql doit être joignable depuis le site).
Choisir l'utilisateur, le mot de passe et le nom de la DB [Ex : yourtrace]

```
mysql -u root -p
```
```
mysql> CREATE DATABASE database_name
```

6. Configurer la connexion à la base de données dans le fichier `.env` :
Exemple :
```
DATABASE_URL="mysql://examplelogin:examplepassword@localhost:3307/database_name"
```
/!\ *Le fichier .env ne doit pas être commit, celui qui se trouve sur le repo est un fichier d'exemple. Ces informations sont propres à votre installation*

7. Une fois la base de données connectée, il ne reste qu'à executer la migration des tables pour les Entités stockées :
```
//A la racine du projet :
php bin/console doctrine:migrations:migrate
```

8. Créer un utilisateur admin :
```
php bin/console app:create-admin
```
Cela insère automatiquement un utilisateur avec le rôle "ADMIN" dans la base de donnée, avec comme identifiants :
- admin@yourtrace.com
- il_faudra_songer_a_changer_cette_passphrase_par_defaut

9. Démarrer le server :
- Symfony-cli :
```
symfony server:start
```

**Le site est consultable à l'adresse 127.0.0.1:8000**

