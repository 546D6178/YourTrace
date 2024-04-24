#!/usr/bin/python3

#==============================================================================
#API LeakLookup
#==============================================================================

import sys
import requests
import re 
import cgi
import json

#email
#if(re.match("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sys.argv[1])):

form = cgi.FieldStorage()
email = form.getvalue("email")
result = form.getvalue("result")
    
#res = os.system(f"curl 'https://leak-lookup.com/api/search' -d 'key=8e0ed734acc7821a5e5066d800f413c9&type=email_address&query={email}'")
reponse = requests.post("https://leak-lookup.com/api/search",{"key":"8e0ed734acc7821a5e5066d800f413c9","type":"email_address","query":email})

fd = open("/var/www/html/result/"+result,"w")
fd.write(json.loads(reponse))
fd.close()

print("Content-type: text/html\n")
print("done")
