#!/usr/bin/env python3

from threading import Thread
import threading
import json
import requests
import time
import cgi

#variable pour le resultat final qui sera renvoye au site
global_result = {}

#verrou pour l'ecriture dans le fichier global
lock = threading.Lock()

#emplacement des fichiers pour chaque type d'outils
tooldata = {"scrapper":"scrapper_tools.json","api":"api_tools.json","direct":"direct_tools.json"}

#thread function for each tool
def tool_thread(tool_type, user_data, tool):
    #get donnees de l'outil
    fd = open("json/"+tooldata[tool_type],"r")
    content = json.loads(fd.read())
    fd.close()

    #get url de l'outil
    url = content[tool]["url"]

    #garde seulement les donnees utiles a l'outil
    input_ = content[tool]["input"]
    user_data_reduced = {}
    for inpt in input_:
        if inpt in user_data:
            user_data_reduced[inpt] = user_data[inpt]

    #prepare les donnes a envoyer
    data_to_send = {}
    for data in user_data_reduced:
        data_to_send[data] = user_data_reduced[data]
    data_to_send["tool_type"] = tool_type
    data_to_send["tool"] = tool
    result = tool_type + "_"  + tool + "_" + list(user_data_reduced.values())[0] + ".json"
    data_to_send["result"] = result
    
    #envoie les donnees a l'outil
    reponse = requests.post(url, data_to_send)
 
    #si la requete fonctionne, recuperer le resultat de l'outil
    if str(reponse) == "<Response [200]>":
        reponse = requests.get("http://10.16.0.6/result/"+result)
        lock.acquire()
        global_result[tool] = json.loads(reponse.text)
        lock.release()


#thread function for each category tool
def cate_thread(tool_type, user_data):
    #get donnees type d'outil
    fd = open("json/"+tooldata[tool_type],"r")
    content = json.loads(fd.read())
    fd.close()

    #get donnees exploitable de l'utilisateur
    exploitableTools = []
    for tool in content:
        dataNeeded = content[tool]["input"]
        exploitable = 1
        for data in dataNeeded:
            if data not in user_data:
                exploitable = 0
            if exploitable and tool not in exploitableTools:
                exploitableTools.append(tool)
    
    threads = []
    
    #lance le thread de chaque outil
    for tool in exploitableTools:
        new_thread = Thread(target=tool_thread, args=(tool_type, user_data, tool))
        new_thread.start()
        threads.append(new_thread)
        #temps d'attente pour eviter conflit entre requetes http
        time.sleep(0.5)
    
    #attend la fin de chaque thread de chaque outil
    for th in threads:
        result = th.join()

form = cgi.FieldStorage()
#recupere toutes les donnees utilisateur
data_user = {}
for key in form.keys():
    data_user[key] = form.getvalue(key)


#start chaque thread de chaque type d'outil
scrapperThread = Thread(target=cate_thread ,args=("scrapper",data_user) )
scrapperThread.start()
#temps d'attente pour eviter conflit entre requetes http
time.sleep(0.5)
APIThread = Thread(target=cate_thread ,args=("api",data_user) )
APIThread.start()
#temps d'attente pour eviter conflit entre requetes http
time.sleep(0.5)
directThread = Thread(target=cate_thread ,args=("direct",data_user) )
directThread.start()

#attendre la fin de chaque thread
scrapperThread.join()
APIThread.join()
directThread.join()


print("Content-type: text/html\n")
print(json.dumps(global_result))
