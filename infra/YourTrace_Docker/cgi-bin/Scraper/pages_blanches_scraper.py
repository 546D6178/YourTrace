#!/usr/bin/python3

#=================================================
# Scraper les Pages Blanches en fonction d'un prénom + nom
# Renvoie les 5 premiers résultats avec nom/prénom, téléphone, adresse
# A executer si seon ne renvoie rien
#
# Format du json de sortie : {nom1:nom1, prenom1:prenom1, telephone1:telephone1, adresse1:adresse1}
# Si aucun résultat, le json de sortie sera : ["No result found"]
#=================================================

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import urllib.request
import json
import sys
import time
import cgi

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



def scraper(prenom, nom, result):

    
## Pass True if you want to hide chrome browser
## Launching chromium
    
    browser = chrome(True)


###### SCRAPING
    resultat = []

    link_search = "https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+prenom+"+"+nom+"&ou=&univers=pagesblanches&idOu="
    
    browser.get(link_search)
    browser.implicitly_wait(3)
    time.sleep(6)
    browser.save_screenshot('pages_blanches.png')

    # Cookies
    try:
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/span').click()
    except:
        pass
    ## premier résultat
    try:    
        element = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[1]/div[1]/div/div/a/h3').text

        if element.lower() == (prenom + ' '+ nom).lower() or element.lower() == (nom + ' '+ prenom).lower() :
            adresse1 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[1]/div[1]/div/div/div/a').text
            button_tel = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[1]/div[2]/button')
            button_tel.click()
            telephone1 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[1]/div[2]/div/div/span').text
            
            
            resultat.append({'nom':element,'adresse1' : adresse1[:-13], 'telephone1' : telephone1})
    except:
        pass

    ## second résultat
    try: 
        element = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[2]/div[1]/a/h3').text

        if element.lower() == (prenom + ' '+ nom).lower() or element.lower() == (nom + ' '+ prenom).lower() :
            adresse2 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[2]/div[1]/a/h3').text
            button_tel = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[2]/div[2]/button').click()
            telephone2 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[2]/div[2]/div/div/span[2]').text

            resultat.append({'nom' : element, 'adresse2' : adresse2[:-13], 'telephone2' : telephone2})
    except:
        pass

    ## Troisième résultat
    try: 
        element = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[3]/div[1]/a/h3').text
        if element.lower() == (prenom + ' '+ nom).lower() or element.lower() == (nom + ' '+ prenom).lower() :
            adresse3 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[3]/div[1]/div/a').text
            button_tel = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[3]/div[2]/button').click()
            telephone3 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[3]/div[2]/div/div/span').text

            resultat.append({'nom': element, 'adresse3' : adresse3[:-13], 'telephone3' : telephone3})
    except:
        pass

    ## Quatrième résultat
    try: 
        element = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[4]/div[1]/a/h3').text
        if element.lower() == (prenom + ' '+ nom).lower() or element.lower() == (nom + ' '+ prenom).lower() :
            adresse4 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[3]/div[1]/div').text
            button_tel = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[4]/div[2]/button').click()
            telephone4 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[4]/div[2]/div/div/span[2]').text

            resultat.append({'nom': element, 'adresse4' : adresse4[:-13], 'telephone4' : telephone4})
    except:
        pass

    ## Cinquième résultat
    try: 
        element = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[5]/div[1]/a/h3').text
        if element.lower() == (prenom + ' '+ nom).lower() or element.lower() == (nom + ' '+ prenom).lower() :
            adresse5 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[5]/div[1]/div').text
            button_tel = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[5]/div[2]/button').click()
            telephone5 = browser.find_element(By.XPATH, '/html/body/main/div[2]/div/section/div/ul/li[5]/div[2]/div/div/span[2]').text

            resultat.append({'adresse5' : adresse5[:-13], 'telephone5' : telephone5})

    except:
        pass
    
    if resultat == []:
        resultat.append("No result found")

    #filename = "pages_blanches_"+prenom+"_"+nom+".json"
    with open("/var/www/html/result/"+result, "w") as f:
        json.dump(resultat, f, ensure_ascii=False)


form = cgi.FieldStorage()
name = form.getvalue("name")
lastname = form.getvalue("lastname")
result = form.getvalue("result")
scraper(name, lastname, result)

print("Content-type: text/html\n")
print("done")

"""
if __name__ == "__main__":

    nb_arg = len(sys.argv[1:])
    if nb_arg == 2:
        prenom = sys.argv[1]
        nom = sys.argv[2]
        scraper(prenom, nom)
    else:
        print("Exemple d'utilisation : python3 pages_blanches_scraper.py prenom nom")
"""
