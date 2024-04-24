#!/usr/bin/python3

#=================================================
# Scraper Duolingo en fonction d'un pseudo 
# Renvoie le lien vers un profil 
# A executer si seon ne renvoie rien
#
# Format du json de sortie : {url:url, status:exist|none}
#=================================================

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.request
import json
import sys
import cgi

def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    #d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument("--remote-debugging-port=9222")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    opt.binary_location = "/usr/bin/google-chrome-stable"
    #try: 
    #    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver-linux64/chromedriver'), use_subprocess=True,options=opt)
    #except NoSuchDriverException:
    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver'), use_subprocess=True,options=opt)
    
    browser.implicitly_wait(10)
    return browser



def scraper(username, result):

    
## Pass True if you want to hide chrome browser
## Launching chromium
    browser = chrome(True)


###### SCRAPING
    resultat = []

    link_search = "https://www.duolingo.com/profile/"+username
    
    browser.get(link_search)
    browser.implicitly_wait(3)


    ## Case profile exist
    try:    
        element = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/h1/div').text
        if username.lower() in element.lower() :
            resultat.append({'url' : 'https://www.duolingo.com/profile/'+username, 'status':'exist'})
       
    ## Case profile inexistant
    except:
        element = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/h1').text

        if '404' in element:
            resultat.append({'url' : "Profile doesn't exist", "status":"none"})


    #filename = "duolingo_"+username+".json"
    with open("/var/www/html/result/"+result, "w") as f:
        json.dump(resultat, f)

form = cgi.FieldStorage()
username = form.getvalue("username")
result = form.getvalue("result")
scraper(username, result)

print("Content-type: text/html\n")
print("done")


"""
if __name__ == "__main__":
    result = "duolingo_test.json"
    nb_arg = len(sys.argv[1:])
    if nb_arg == 1:
        username = sys.argv[1]
        scraper(username, result)
    else:
        print("Exemple d'utilisation : python3 duolingo_scraper.py username")
"""
