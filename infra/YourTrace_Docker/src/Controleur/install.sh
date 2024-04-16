#!/bin/bash

git config --global http.https://44.211.92.107/.sslVerify false && \
git clone https://tmax:glpat--znxqv6UyBGz7baBy8M8@44.211.92.107/yourtrace/integration_tools.git && \
mv ./integration_tools/Controleur/controleur_scrapper.py /usr/lib/cgi-bin/ && \
mv ./integration_tools/Controleur/json /usr/lib/cgi-bin/ && \
rm -rf ./integration_tools
