#!/usr/bin/python3

#==============================================================================
#API LeakLookup
#==============================================================================

import sys
import requests
import re 
import cgi
import json

#nom prénom ("prénom nom")
#if(re.match(r"(?u)^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð'\-]+\s[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð'\-\s]+$", sys.argv[1])):

form = cgi.FieldStorage()
name = form.getvalue("name")
lastname = form.getvalue("lastname")
query = name + " " + lastname
result = form.getvalue("result")

#res = os.system(f"curl 'https://leak-lookup.com/api/search' -d 'key=8e0ed734acc7821a5e5066d800f413c9&type=fullname&query={query}'")
reponse = requests.post("https://leak-lookup.com/api/search",{"key":"8e0ed734acc7821a5e5066d800f413c9","type":"fullname","query":query})

fd = open("/var/www/html/result/"+result,"w")
fd.write(json.loads(reponse))
fd.close()


print("Content-type: text/html\n")
print("done")

