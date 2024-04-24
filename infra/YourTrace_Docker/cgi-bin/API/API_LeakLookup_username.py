#!/usr/bin/python3

#==============================================================================
#API LeakLookup
#==============================================================================

import sys
import requests
import re 
import cgi
import json

#username
#elif(re.match("^[A-Za-z0-9\_\-\*]+(?:[ _-][A-Za-z0-9]+)*$", sys.argv[1])):

form = cgi.FieldStorage()
username = form.getvalue("username")
result = form.getvalue("result")

#res = os.system(f"curl 'https://leak-lookup.com/api/search' -d 'key=8e0ed734acc7821a5e5066d800f413c9&type=username&query={username}'")
reponse = requests.post("https://leak-lookup.com/api/search",{"key":"8e0ed734acc7821a5e5066d800f413c9","type":"username","query":email})

fd = open("/var/www/html/result/"+result,"w")
fd.write(json.loads(reponse))
fd.close()


print("Content-type: text/html\n")
print("done")

