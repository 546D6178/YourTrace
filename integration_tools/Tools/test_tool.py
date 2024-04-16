### A ajouter au debut de l'outil pour recuperer les valeurs ###
### Pour recuperer une valeur : form.getvalue("name") ------ ###
#!/usr/bin/python3
import cgi
form = cgi.FieldStorage()
result = form.getvalue("result")
data = "le nom recupere : " + form.getvalue("name") + " --donnees test-- "
### -------- Fin de la partie a ajouter au debut outil -------- ###

### Simulation du travail d'un outil ###
import random
import time
pause = random.randint(1,6)
time.sleep(pause)
### --- Fin simulation de l'outil -- ###

### A ajouter a la fin de l'outil pour mettre a disposition les resultats ###
### Ecrire le resultat dans le fichier "result" dans "/var/www/html/result/result"
fd = open("/var/www/html/result/"+result,"w")
fd.write(data)
fd.close()
### -------- Fin de la partie a ajouter a la fin outil -------- ###

print("Content-type: text/html\n\n")
print("resultats accessible a http://IP/result/"+result)

