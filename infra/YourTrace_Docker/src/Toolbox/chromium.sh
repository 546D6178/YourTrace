#!/bin/bash

#apt update 
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt --fix-broken install -y
#curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/\
#$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")/chromedriver_linux64.zip"



#wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chromedriver-linux64.zip


curl --silent "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
  | jq --arg majorVersion "$CHROME_MAJOR_VERSION" -r '.channels.Stable | select(.version | startswith($majorVersion | tostring)).downloads.chromedriver[] | select(.platform == "linux64") | .url' \
  | xargs curl -L --show-error --silent --output chromedriver-linux64.zip


mkdir -p "chromedriver/stable"
unzip -q "chromedriver-linux64.zip" -d "chromedriver/stable"
mv /chromedriver/stable/chromedriver-linux64/chromedriver /chromedriver/stable/
chmod +x "chromedriver/stable/chromedriver"

rm chromedriver_linux64.zip && rm googlels-chrome-stable_current_amd64.deb
