#!/usr/bin/python3

#=================================================
# Scraper Discord en fonction d'un pseudo
# Renvoie le lien vers un profil
# A executer si seon ne renvoie rien
#
# Format du json de sortie : {url:url, location:location, occupation:occupation, pronom:pronom, gender:gender, social1:social1, social2:social2, social3:social3, bio:bio, birthday:birthday}
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

import undetected_chromedriver as uc
"""
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
    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver'),options=opt)
    
    browser.implicitly_wait(10)
    return browser
"""
def chrome(headless=False):
    # support to get response status and headers
#    d = uc.DesiredCapabilities.CHROME
#    d['loggingPrefs'] = {'performance': 'ALL'}

    opt = uc.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument("--remote-debugging-port=9222")
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument("--disable-popup-blocking")
    opt.binary_location = "/usr/bin/google-chrome-stable"
    #try: 
    #    browser = uc.Chrome(service=Service('/chromedriver/stable/chromedriver-linux64/chromedriver'), use_subprocess=True,options=opt)
    #except NoSuchDriverException:
    browser = uc.Chrome(service=Service('/chromedriver/stable/chromedriver'), use_subprocess=True,options=opt)
    browser.implicitly_wait(10)
    return browser



def scraper(username, result):

    
## Pass True if you want to hide chrome browser
## Launching chromium
    browser = chrome(True)


###### SCRAPING
    resultat = []

    link_search = "https://discords.com/bio/p/"+username
    
    browser.get(link_search)
    browser.implicitly_wait(3)


    ## Case profile exist but status is private
    try:    
        element = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div/h1').text
        resultat.append({'url' : 'https://discords.com/bio/p/'+username })
        
        
        # Collecte des informations pas toujours presentes  
        # Location
        try : 
            location  = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[5]/div/div[2]/div[2]').text
            resultat.append({'location':location, 'status':'exist'})
        except:
            resultat.append({'status': 'does not exist'})
            with open("/var/www/html/result/"+result, "w") as f:
                json.dump(resultat, f)
            
            return
        # Bio
        try:
            bio = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/div/div[2]/div').text
            resultat.append({'bio':bio})    
        except:
            pass

        # Occupation
        try:
            occupation = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]').text
            resultat.append({'occupation':occupation})
        except:
            pass

        # Birthday
        try:
            birthday = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[3]/div/div[2]/div[2]').text
            resultat.append({'birthday':birthday})
        except:
            pass
        # Gender
        try:
            gender = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[6]/div/div[2]/div[2]').text
            resultat.append({'gender':gender})
        except:
            pass
        # Language Spoken
        try :
            language = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[4]/div/div[2]/div[2]').text
            resultat.append({'language':language})
        except:
            pass

        # Pronom
        try:
            pronom = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[7]/div/div[2]/div[2]').text
            resultat.append({'pronom':pronom})
        except:
            pass

        # Social Media
        try:
            social1 = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[8]/div/div[2]/div/div/div[1]/div/div/div[2]/a').get_attribute("href")
            resultat.append({'social1':social1})
        except:
            pass
        try:
            social2 = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[8]/div/div[2]/div/div/div[2]/div/div/div[2]/a').get_attribute("href")
            resultat.append({'social2':social2})
        except:
            pass
        
        try:
            social3 = browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[8]/div/div[3]/div/div/div[2]/div/div/div[2]/a').get_attribute("href")
            resultat.append({"social3":social3})
        except:
            pass

    ## Cas profile inexistant
    except:
        resultat.append({'url' : "Profile doesn't exist"})

    #filename = "discord_"+username+".json"
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
    result = "discord_test.json"
    nb_arg = len(sys.argv[1:])
    if nb_arg == 1:
        username = sys.argv[1]
        scraper(username, result)
    else:
        print("Exemple d'utilisation : python3 discord_scraper.py username")
"""
