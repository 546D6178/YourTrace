#!/usr/bin/python3

import os
import sys
import re
import json
import cgi
#====================#
#       IGNORANT     #
#====================#

form = cgi.FieldStorage()
phone = form.getvalue("phone")
result = form.getvalue("result")


#Num tél : 33 xxxxxxxxx
#if(re.match("^33\s[0-9]+$", sys.argv[1])): 
resultat = os.system("cd ignorant && ignorant "+phone)
sys.exit()
    
#filename = "ignorant_"+sys.argv[1]+".json"
with open("/var/www/html/result/"+result, "w") as f:
    json.dump(resultat.json(), f)

print("Content-type: text/html\n")
print("done")

    
