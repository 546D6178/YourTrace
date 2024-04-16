#!/bin/bash

red='\033[0;31m'
reset='\033[0m'
green='\033[0;32m'

if ls /usr/bin/docker 1> /dev/null 2>&1 && ls /usr/bin/docker-compose 1> /dev/null 2>&1; then
	echo -e "${green}Docker et Docker-compose OK${reset}"
else
	echo -e "${red}Veuillez installer docker et docker-compose${reset}"
	exit 1
fi

dossier="../../website"

if [ -d "$dossier" ]; then
	echo -e "${green}Le dossier Website existe.${reset}"
	echo -e "${green}Fetch en cours.${reset}"
	/bin/bash -c "cd ../../website/ && git config --global http.https://43.211.92.107/.sslVerify false && git fetch"
	if [[ $(/bin/bash -c "cd ../../website/ && git rev-parse dev 2>&1") != $(/bin/bash -c "cd ../../website/ && git rev-parse origin/dev") ]]; then 
		echo -e "${red}Attention branche DEV du dossier website pas à jour${reset}."	
		read -e -p "Voulez-vous pull les dernières mises à jour ? ATTENTION CELA VA ECRASER VOS MODIFICATIONS ACTUELLES du dossier WEBSITE. DEFAULT no (yes/no): " -i "no" choice
		if [ "$choice" = "yes" ]; then
			# Actions à effectuer si l'utilisateur choisit "yes"
			echo -e "${green} GIT PULL INCOMING from DEV .${reset}"
			/bin/bash -c "cd ../../website/ && git checkout dev && git pull"
			if [ $? -ne 0 ]; then
					echo -e "${red}La commande GIT a échouée. Sortie du script.${reset}"
					exit 1
			fi
		elif [ "$choice" = "no" ]; then
			# Actions à effectuer si l'utilisateur choisit "no"
			echo -e "${red}No? Ok.. Maybe later? ${reset}\n"	
		else
			# Actions à effectuer si l'utilisateur donne une réponse non attendue
			echo -e "${red}\"yes\" or \"no\" not !d%f%bnhgjtyc please.${reset}"
			exit 1
		fi
	fi

	if [[ $(/bin/bash -c "cd ../../website/ && git rev-parse main 2>&1 ") != $(/bin/bash -c "cd ../../website/ && git rev-parse origin/main") ]]; then 	
		echo -e "${red}Attention branche MAIN du dossier website pas à jour${reset}.\n"	
		read -e -p "Voulez-vous pull les dernières mises à jour ? ATTENTION CELA VA ECRASER VOS MODIFICATIONS ACTUELLES du dossier WEBSITE. DEFAULT no (yes/no): " -i "no" choice
		if [ "$choice" = "yes" ]; then
			# Actions à effectuer si l'utilisateur choisit "yes"
			echo -e "\n${green} GIT PULL INCOMING from MAIN .${reset}"
			/bin/bash -c "cd ../../website/ && git checkout main && git pull"
			if [ $? -ne 0 ]; then
					echo -e "${red}La commande GIT a échouée. Sortie du script.${reset}"
					exit 1
			fi
		elif [ "$choice" = "no" ]; then
			# Actions à effectuer si l'utilisateur choisit "no"
			echo -e "${red}No? Ok.. Maybe later?${reset}\n"

		else
			# Actions à effectuer si l'utilisateur donne une réponse non attendue
			echo -e "${red}\"yes\" or \"no\" not !d%f%bnhgjtyc please..${reset}"
			exit 1
		fi
	fi
else
	echo -e "${red}Le dossier Website est introuvable.${reset}"
	read -p "Voulez-vous le créer ? (yes/no): " choice
	if [ "$choice" = "yes" ]; then
    		# Actions à effectuer si l'utilisateur choisit "yes"
    		echo -e "${green} GIT CLONE INCOMING FROM MAIN .${reset}"
		git config --global http.https://44.211.92.107/.sslVerify false && \
		git clone https://44.211.92.107/yourtrace/website.git ../../website
		if [ $? -ne 0 ]; then
   			echo -e "${red}La commande GIT a échouée. Sortie du script.${reset}"
    			exit 1
		fi
	elif [ "$choice" = "no" ]; then
    		# Actions à effectuer si l'utilisateur choisit "no"
    		echo -e "${red}No ? Ok bye.${reset}"
		exit 1
	else
    		# Actions à effectuer si l'utilisateur donne une réponse non attendue
    		echo -e "${red}\"yes\" or \"no\" not !d%f%$bnhgjty$c please.${reset}"
		exit 1
	fi
fi

cp "sample.env" ".env"

read -e -p "Build l'image du website depuis quelle branche ? DEFAULT dev (main/dev): " -i "dev" choice
if [ "$choice" = "main" ]; then
	/bin/bash -c "cd ../../website && git checkout -q main"
elif [ "$choice" = "dev" ]; then
	/bin/bash -c "cd ../../website && git checkout -q dev"
else
	# Actions à effectuer si l'utilisateur donne une réponse non attendue
	echo -e "${red}\"dev\" or \"main\" not !d%f%$bnhgjty$c please.${reset}"
	exit 1
fi

echo -e "${green}Build des images.${reset}"

read -e -p "Build les images avec le cache de docker ? Ne pas utiliser le cache permet d'être sur d'avoir tous les fichiers des instructions COPY ou ADD  mais peut être long  DEFAULT no (yes/no): " -i "no" choice
if [ "$choice" = "yes" ]; then
        docker-compose build --no-cache
elif [ "$choice" = "no" ]; then
	docker-compose build #--no-cache
else
        # Actions à effectuer si l'utilisateur donne une réponse non attendue
        echo -e "${red}\"no\" or \"yes\" not !d%f%$bnhgjty$c please.${reset}"
        exit 1
fi


if docker ps -a | grep -q YourTrace- ; then
	#docker ps | grep YourTrace- | xargs docker stop  1>/dev/null 2>&1
	echo -e "\n${green}Suppression des anciens conteneurs.${reset}\n"
	docker ps -a | grep "YourTrace-" | awk '{print $1}' | xargs -I {} docker stop {}
	docker ps -a | grep "YourTrace-" | awk '{print $1}' | xargs -I {} docker rm {}
	docker-compose up -d --force-recreate
else
	docker-compose up -d
fi

#6 est le nombre actuel de conteneur attendu 
if [ $(docker ps | grep "YourTrace-" | wc -l) = "6" ]; then
	echo -e "\n${red}Attention${reset}, l'execution de ce script créer un volume de log dans ${red}./volumes_yourtrace/logs/${reset}\n"
	echo -e "${green}Voici les conteneurs de YourTrace ! : ${reset}\n"
	echo -n "$(yes "═" | head -n ${COLUMNS}  | tr -d '\n')"
	echo -e "\n"
	docker ps | awk 'NR==1 || /YourTrace-/'
	echo -e "\n"
	echo -n "$(yes "═" | head -n ${COLUMNS}  | tr -d '\n')"
	echo -e "\n${green}L'interface Web est accessible à http://localhost:8100${reset}"
else
	echo -e "${red}Un probleme s'est produit, l'un des conteneurs necessite plus d'attention${reset}" 
fi 
