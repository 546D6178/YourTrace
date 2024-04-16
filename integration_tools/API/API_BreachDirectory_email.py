#==============================================================================
# API BreachDirectory
#==============================================================================

#==============================================================================
# ATTENTION : 10 REQUETES PAR MOIS 
# NE PAS EXECUTER POUR LE FUN
#==============================================================================

#==============================================================================
#
# Prend en entrée un mail
# Rend en sortie un JSON (voir exemple dans le dossier controleur>json>breachdirectory_example.json)
#
#==============================================================================

import requests
import sys
import cgi
import json

url = "https://breachdirectory.p.rapidapi.com/"

querystring = {"func":"auto","term":"{sys.argv[1]}"}

headers = {
 	"X-RapidAPI-Key": "cb73804857msh6b8554faac1d827p1eedccjsn1a42562c5264",
 	"X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
 }

result = requests.get(url, headers=headers, params=querystring)

final_res = result.json()

filename = "apibreach_"+sys.argv[1]
with open("/var/www/html/result/"+filename, "w") as f:
	json.dump(result.json(), f)

print("Content-type: text/html\n")
print("done")
