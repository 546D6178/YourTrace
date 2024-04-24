#!/usr/bin/python3

#====================#
#       H8MAIL       #
#====================#
import re
import os
import sys
import cgi

form = cgi.FieldStorage()
email = form.getvalue("email")
result = form.getvalue("result")


#email 
#if(re.match("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", sys.argv[1])):
result = os.system("cd h8mail && h8mail -t "+ email +" -j /var/www/html/result/" + result + ".json")

print("Content-type: text/html\n")
print("done")

