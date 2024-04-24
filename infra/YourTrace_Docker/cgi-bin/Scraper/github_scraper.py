#!/usr/bin/python3

#=================================================
# Scraper Github en fonction d'un username afin d'obtenir l'adresse mail
#   - Gestion des erreurs lors du crash au lancement du Chrome + au moment du get 
#=================================================
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service ##
import urllib.request
import zipfile
import json
import sys
import cgi
import traceback
import re

print("Content-type: text/html\n")

def chrome(headless=False):
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
   # d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument("--remote-debugging-port=9222")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_argument("--disable-popup-blocking")
    opt.add_argument('./plugin.zip')
    opt.binary_location = "/usr/bin/google-chrome-stable"######
    #try: 
    #    browser = webdriveruc.Chrome(service=Service('/chromedriver/stable/chromedriver-linux64/chromedriver'), use_subprocess=True,options=opt)
    #except NoSuchDriverException:
    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver'), use_subprocess=True,options=opt)
    
    browser.implicitly_wait(10)
    return browser


def scraper(username, result):

## Pass True if you want to hide chrome browser
## Launching chromium
    repo_liste = []
    browser = chrome(True)
    print("Browser Launch")
# Attempting to access github profile
    try:
        print("Accessing profile...")
        browser.get('https://github.com/' + username + '?tab=repositories')
    except:
        resultats.append("No result found")
        return

    # Retrieve and navigate to the first repo
    try:
        repo1 = browser.find_element(By.XPATH,'/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[1]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo1)
    except:
        print("No repo for this user !")
        return

    # Retrieve other repo
    try:
        print("Collecting all repos link...")
        repo2 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[2]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo2)
        repo3 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[3]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo3) 
        repo4 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[4]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo4) 
        repo5 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[5]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo5)
        repo6 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[6]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo6)
        repo7 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[7]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo7)
        repo8 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[8]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo8)
        repo9 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[9]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo9)
        repo10 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[10]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo10)
        repo11 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[11]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo11)
        repo12 = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/main/div[2]/div/div[2]/turbo-frame/div/div[2]/ul/li[12]/div[1]/div[1]/h3/a').get_attribute("href")
        repo_liste.append(repo12)

    except: 
        pass

    # Loop in repo for retrieving all emails address
    email_liste = []
    email_unique = []
    for repo in repo_liste:
        try:
            print("Accessing commit...")
            # Navigate to repo
            browser.get(repo)
            print(browser.current_url)
            # Navigate to commit
            element = browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/main/turbo-frame/div/div/div/div[2]/div[1]/react-partial/div/div/div[1]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[1]/div/table/tbody/tr[1]/td/div/div[2]/div[1]/span[1]/a')
            commit_link = element.get_attribute('href')
            #print(commit_link)

            # Accessing .patch
            print("Accessing .patch...")
            browser.get(commit_link + '.patch')
            texte = browser.find_element(By.XPATH, '/html/body/pre').text
    
            # Parse texte
            print("Retrieving email...")
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_liste.extend(re.findall(email_pattern, texte))
            #print(email_liste) 
        except:
            pass
    
    print("Cleaning collected emails...")
    # Only unique email
    for email in email_liste:
        if email not in email_unique and "github" not in email:
            email_unique.append(email)

    print(email_unique)
    print("Json Formating...")
    # Store Results in List of Dict
    dico = {'URL':"https://github.com/"+ username, 'username': username, 'emails':email_unique}

 
#### Processing results in JSON
    print("Writing in /var/www/html/result/"+result)
    #filename = "github_"+username.json"
    with open("/var/www/html/result/"+result, "w") as f:
        json.dump(dico, f, ensure_ascii=False)


# MAIN

form = cgi.FieldStorage()
username = form.getvalue("username")
result = form.getvalue("result")

scraper(username, result)
print("done")

# FOR TESTING
"""
if __name__ == "__main__":
    result = "github_test.json"
    nb_arg = len(sys.argv[1:])
    if nb_arg == 1:
        username = sys.argv[1]
        scraper(username, result)

    else:
        print("Exemple d'utilisation : python3 github_scraper.py username")

print("done")
"""
