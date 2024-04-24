#!/usr/bin/python3

#=================================================
# Scraper Linkedin en fonction d'un Prénom et d'un Nom
# Nécessite un compte (config.txt)
# Renvoie la liste des profils correspondants à la recherche
# A executer si seon ne renvoie rien
# TO DO :
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
    #    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver-linux64/chromedriver'), use_subprocess=True,options=opt)
    #except NoSuchDriverException:
    browser = webdriver.Chrome(service=Service('/chromedriver/stable/chromedriver'), use_subprocess=True,options=opt)
    
    browser.implicitly_wait(10)
    return browser



def scraper(prenom, nom, result):

    
## Pass True if you want to hide chrome browser
## Launching chromium
    browser = chrome(True)
    print("Browser Launch")
# Attempting to inject cookies to avoid authentification
    browser.get('https://www.linkedin.com/uas/login')
    try:
        ## Cookies
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        
        cookie_a_injecter = None
        for cookie in cookies:
            if cookie['name'] == 'li_at':
                cookie_a_injecter = cookie
                break

        if cookie_a_injecter:
            print(cookie_a_injecter)
            browser.add_cookie(cookie_a_injecter)
            print("Cookie injecté")
        else:
            print("Cookie pas trouvé")
            
        browser.get('https://www.linkedin.com/feed/')
        
        try:
            element = browser.find_element(By.ID, "ember28")
            print("Cookies OK")
        except NoSuchElementException:
            print("Cookies KO")
            
    except Exception as e:
        print("Trying old school connection")
        #browser.quit()
        # Go to Linkedin Auth
        browser.get('https://www.linkedin.com/uas/login')
        # Wait 3
        browser.implicitly_wait(3)
        # Reading Credentials
        file = open('config.txt')
        lines = file.readlines()
        username = lines[0]
        password = lines[1]

        # Authentification 
        elementID = browser.find_element(By.ID,'username')
        elementID.send_keys(username)

        elementID = ""
        elementID = browser.find_element(By.ID,'password')
        if(elementID == ""):
            print("Element not found")

        elementID.send_keys(password)
        print("Authentication OK")

        # Recuperation de la session

        print("Enregistrement des cookies")
        
        cookies = browser.get_cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)



###### SCRAPING
    info = []

    link_search = "https://www.linkedin.com/search/results/people/?keywords="+prenom+"%20"+nom+"&origin=SWITCH_SEARCH_VERTICAL&sid=I~o"
    links = [link_search]

# Get the page (link by link)

    for link in links:
        browser.get(link)
        browser.implicitly_wait(1)

        print("I access the search page")
        print(browser.page_source)
#########################################
#
# Parse
#
#########################################

        resultats = []

# URL profile
        try:
            url_profile = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a")
            final_url = url_profile.get_attribute("href")
            print("final_url : "+final_url)

# Name

            name_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a/span/span[1]")
            name = name_search.text
            print("name : "+name)

# Job

            job_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div/div[2]")
            job = job_search.text
            print("job : "+job)
        
# Location

            location_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div/div[3]")
            location = location_search.text
            print("location : " +location)
            print("I've found result")
   
# Store Results in List of Dict
            dico = {'URL':final_url, 'Name': name, 'job':job, 'location':location}
            resultats.append(dico)

            print("Save results to dico ok")

        except:
            print("No result found")

        try:
#### URL 2
            url_profile = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[2]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a")
            final_url = url_profile.get_attribute("href")

# Name

            name_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[2]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a/span/span[1]")
            name = name_search.text

# Job

            job_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[2]/div/div/div/div[2]/div/div[2]")
            job = job_search.text
    
# Location

            location_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[2]/div/div/div/div[2]/div/div[3]")
            location = location_search.text
    
        # Store Results in List of Dict
            dico = {'URL':final_url, 'Name': name, 'job':job, 'location':location}
            resultats.append(dico)

        except:
            pass

#### URL 3
        try:
            url_profile = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[3]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a")
            final_url = url_profile.get_attribute("href")

# Name

            name_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[3]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a/span/span[1]")
            name = name_search.text

# Job

            job_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[3]/div/div/div/div[2]/div/div[2]")
            job = job_search.text
    
# Location

            location_search = browser.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[3]/div/div/div/div[2]/div/div[3]")
            location = location_search.text

# Store Results in List of Dict
            dico = {'URL':final_url, 'Name': name, 'job':job, 'location':location}
            resultats.append(dico)

        except:
            pass

#### Processing results in JSON
        #filename = "linkedin_"+prenom+"_"+nom+".json"
        with open("/var/www/html/result/"+result, "w") as f:
            json.dump(resultats, f, ensure_ascii=False)


form = cgi.FieldStorage()
prenom = form.getvalue("name")
nom = form.getvalue("lastname")
result = form.getvalue("result")
#prenom = "Emma"
#nom = "SANCHEZ"
#result = "scrapper_linkedin_scraper_Emma_SANCHEZ.json"
scraper(prenom, nom, result)


print("done")

"""
if __name__ == "__main__":
    result = "linkedin_test.json"
    nb_arg = len(sys.argv[1:])
    if nb_arg == 2:
        prenom = sys.argv[1]
        nom = sys.argv[2]
        scraper(prenom, nom, result)

    else:
        print("Exemple d'utilisation : python3 linkedin.py Prenom NOM")
"""
