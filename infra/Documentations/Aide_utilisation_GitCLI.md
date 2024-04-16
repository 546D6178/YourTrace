
# Avant X opérations 

- Se mettre sur la branche dev puis récupérer les derniers changements de la branche dev (pour mettre à jour votre repo local en fonction du repo distant)

```
cd project_name (infra, website... )
git checkout dev
git pull
```

# Comment git push ? 

- Vérifier la branche sur laquelle on se trouve avant de push : 

`git branch -a # lister les branches et voir celle sur laquelle on se trouve`

- Puis push : 

```
git add ./directory_to_push
git commit -am "tag_pour_commit"
git status # pour avoir plus d'information sur les fichiers ajoutés au commit
git push 
```


# Autres cas 

-  Créer une nouvelle branche

`git checkout -b <branch_name>`

- Si la branche n'est pas encore présente sur GitLab, il faut la créer avant de la pousser. Une seule commande permet de faire les deux en même temps

`git push --set-upstream origin <branch_name>`


