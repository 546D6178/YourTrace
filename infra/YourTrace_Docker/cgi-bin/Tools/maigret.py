#!/usr/bin/python3
#====================#
#       MAIGRET      #
#====================#
""" Update 14/12/2023

- Epuration du code
- Restrictions des recherche sur les 100 meilleurs sites (classement by maigret)
- Récupération de l'username via CGI

"""
#Ex  cution du programme : python maigret.py "username"
#Cr  ation du fichier dans /var/www/html/result
#Output : sortie du fichier en json : report_USERNAME_ndjson.json

import sys
import pathlib
import subprocess
import cgi
import json

#print("Content-type: text/html\r\n")

result_path = '/tmp/'

# Récupération de l'username depuis le site
form = cgi.FieldStorage()
username = form.getvalue("username")
#username = form.getvalue("username")
# username = 'yurikhan'

"""
Check si result_path existe
Lance le Maigret installer localement -> output dispo dans {result_path}
"""
#print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
if pathlib.Path(result_path).is_dir():
    try:
        subprocess.run(["/usr/local/bin/maigret", username, "--top-site", "100", "-J", "simple", "--folderoutput", result_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        #print("Content-type: text/html\n")
        #print("done")
    except subprocess.CalledProcessError as e:
        #print("[MAIGRET] Erreur:", e)
        sys.exit(1)
else:
    #print(f"[MAIGRET] Erreur: le path \"{result_path}\" n'existe pas ..")
    sys.exit(1)

output_json = "report_" + username  + "_simple.json"

fd = open(result_path + output_json)
text = fd.read()
fd.close()
data = json.loads(text)


#get site result
result = {}
all_keys = data.keys()
for key in all_keys:
    result[key] = "account exists"

final_result = []
final_result.append(result)

#output for controlleur
result_name = form.getvalue("result")

with open("/var/www/html/result/" + result_name, "w") as file:
    json.dump(final_result, file, indent=4)  
"""
fd = open("/var/www/html/result/" + result_name, "w")
fd.write(str(final_result))
fd.close()
"""
print("Content-type: text/html\r\n")
print("done")
