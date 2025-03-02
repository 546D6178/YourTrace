#!/bin/bash


chown -R www-data:www-data /usr/lib/cgi-bin/ && chmod +x -R /usr/lib/cgi-bin/ 
#rm -rf ./integration_tools

unzip /usr/lib/cgi-bin/maigret.zip -d /usr/local/lib/python3.10/dist-packages/maigret/
rm -r /usr/lib/cgi-bin/maigret.zip
