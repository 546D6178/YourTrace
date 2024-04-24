#==============================================================================
#API Seon
#==============================================================================

#==============================================================================
# Prend en entrée un numéro de téléphone ou un mail
# En sortie, un JSON disponible
#==============================================================================
import requests
import re
import json
import sys
import cgi

#num tél : +33xxxxxxxxx
if(re.match("^\+\d*", sys.argv[1])):
    headers = {
        "X-API-KEY": "594e10c7-91ec-411c-acd1-1f2b11f0939d"
    }

    result = requests.get(f"https://api.seon.io/SeonRestService/phone-api/v1.4/{sys.argv[1]}", headers=headers)

    filename = "apiseon_"+sys.argv[1]
    with open("/var/www/html/result/"+filename, "w") as f:
        json.dump(result.json(), f)


    print("Content-type: text/html\n")
    print("done")
