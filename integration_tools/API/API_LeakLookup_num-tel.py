#!/usr/bin/python3

#==============================================================================
#API LeakLookup
#==============================================================================

import sys
import requests
import re 
import cgi
import json

#num tél : 07xxxxxxxx
#elif(re.match("\d*$", sys.argv[1])):


form = cgi.FieldStorage()
phone = form.getvalue("phone")
result = form.getvalue("result")

#res = os.system(f"curl 'https://leak-lookup.com/api/search' -d 'key=8e0ed734acc7821a5e5066d800f413c9&type=phone&query={phone}'")
reponse = requests.post("https://leak-lookup.com/api/search",{"key":"8e0ed734acc7821a5e5066d800f413c9","type":"phone","query":phone})

fd = open("/var/www/html/result/"+result,"w")
fd.write(json.loads(reponse))
fd.close()


print("Content-type: text/html\n")
print("done")


