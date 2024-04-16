#!/bin/bash

git config --global http.https://44.211.92.107/.sslVerify false && \
git clone https://tmax:glpat--znxqv6UyBGz7baBy8M8@44.211.92.107/yourtrace/integration_tools.git && \
mv ./integration_tools/API ./integration_tools/Tools ./integration_tools/Scraper /usr/lib/cgi-bin/ && \
chown -R www-data:www-data /usr/lib/cgi-bin/ && chmod +x -R /usr/lib/cgi-bin/ 
rm -rf ./integration_tools

unzip /usr/lib/cgi-bin/maigret.zip -d /usr/local/lib/python3.10/dist-packages/maigret/
rm -r /usr/lib/cgi-bin/maigret.zip
