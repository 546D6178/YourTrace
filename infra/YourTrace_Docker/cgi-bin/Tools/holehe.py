#!/usr/bin/python3

#====================#
#       HOLEHE       #
#====================#
import re
import json
import os
import sys
import csv
import shutil
import cgi
import time

print("Content-type: text/html\n")


def extract_data_to_json(filenameTXT, filenameJSON):
    data = {}
    with open(filenameTXT, 'r') as file:
        content = file.read()

        content_result = " ".join(content.split("[+]")[1:]).split("Email used")[0].split("\n")#content.split("*************")[1].split("[+] Email used")[0].strip()
    
        for output in content_result:
            if(output.strip() != ""):
                data[output.strip()] = "account exists"
    
    final_data = []
    final_data.append(data)
    
    with open(filenameJSON, "w") as file:
        json.dump(final_data, file, indent=4)     
        
    
    
form = cgi.FieldStorage()

#Regex
if(re.match("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", form.getvalue("email"))):
    email = form.getvalue("email")
    result = form.getvalue("result")


#exécuter le fichier : python holehe.py "email"
#Création d'un fichier en csv puis conversion en json

filenameTXT = "holehe_" + email + "_result.txt"

resultat = os.system("holehe " + email + " --only-used 1>" + filenameTXT)

filenameJSON = result
extract_data_to_json(filenameTXT,filenameJSON)

#move json to html repo
if(os.path.exists("/var/www/html/result/"+filenameJSON)):
    os.remove("/var/www/html/result/"+filenameJSON)    
shutil.move(filenameJSON, "/var/www/html/result/")

#remove result in txt file
os.remove(filenameTXT)

#print("Content-type: text/html\n")
print("done")
