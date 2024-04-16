# Pour restore, utiliser ce script : 

```
#!/bin/bash
HASHED_FOLDER=bkp_rasp/srv/gitlab2/data/git-data/repositories/@hashed
RESTORE_FOLDER=test_backup_from_hased

ls $HASHED_FOLDER |while read folder
do
        ls $HASHED_FOLDER/$folder |while read subfolder
        do
                ls $HASHED_FOLDER/$folder/$subfolder |grep -v wiki |while read projectPath
                do
                        fullpath=$(cat $HASHED_FOLDER/$folder/$subfolder/$projectPath/config |grep fullpath |cut -d"=" -f2 |xargs)
                        echo "restoring $fullpath"
                        mkdir -p $RESTORE_FOLDER/$fullpath
                        cp -r $HASHED_FOLDER/$folder/$subfolder/$projectPath/* $RESTORE_FOLDER/$fullpath/
                done
        done
done
```
# Après, il faut git clone mais un repo local 

L'export effectué grâce à ce script ne permet pas de récupérer directement tous les fichiers en un format "lisible". 

## git clone from *local bare* repository

Ce placer dans un dossier exporté de $RESTORE_FOLDER, puis : `git init --bare FOLDER` pour initialiser le repo git

Puis tu peux `git clone FOLDER /dest/path/`

`git --work-tree . reset --hard HEAD` : permet de télécharger directement tous les fichiers, et pas juste "pré-charger". 
