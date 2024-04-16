# Introduction 

Le but ici est de mettre à disposition un service sur le port 443 en utilisant un adresse ip publique d'AWS. 

La création de la machine sur AWS (t2.micro élligible au free tier) ne sera pas abordée. 

## Installation du serveur Openvpn 

`wget https://git.io/vpn -O openvpn-install.sh`

`sudo chmod +x openvpn-install.sh`

`sudo bash openvpn-install.sh`

Récupérer la conf créée lors de l'installation pour la machine souhaitée. 

Ouvrir le port 1194 (udp) pour le fonctionnement du VPN, puis le port 443 pour la redirection du trafic https depuis la console AWS. (source 0.0.0.0/0)

### Asigner une adresse IP fixe à une configuration VPN 
```
sudo mkdir /etc/openvpn/ccd
sudo mkdir /etc/openvpn/ccd/nom_conf_client
```

- Uncomment the line containing client config parameter in server.conf : 

`sudo nano /etc/openvpn/server.conf`

*client-config-dir ccd*

`sudo nano /etc/openvpn/ccd/nom_conf_client`

*ifconfig-push 10.8.0.2 255.255.255.255* 

`sudo /etc/init.d/openvpn restart`


## Paramétrage des règles de firewall


- Se rendre dans sysctl.conf : nano /etc/sysctl.conf

- Dé-commenter la ligne net.ipv4.ip_forward=1

- Appliquer la configuration : sysctl -p


- Ajoutez ces 4 règles de firewall sur le serveur OpenVPN : 

```
sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 10.8.0.2

sudo iptables -A FORWARD -p tcp --dport 443 -d 10.8.0.2 -j ACCEPT

sudo iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo iptables -t nat -A POSTROUTING -p tcp --dport 443 -j SNAT --to 172.31.12.89.89
```
>10.8.0.2 : machine dans le lan vpn vers laquelle je veux rediriger le trafic https

>172.31.12.89.89 : serveur openvpn dans le Lan AWS privée. 

### Assurer le redémarrage du Tunnel VPN lors du reboot du client 

## Création d'un service côté client 

`sudo nano /etc/systemd/system/vpnyourtrace.service`

```
[Unit]
Description=Start tunnel at boot for yourtrace gitlab project
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/openvpn --config /etc/openvpn/tmax.ovpn
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`sudo systemctl daemon-reload`

`sudo systemctl enable vpnyourtrace.service`

`sudo systemctl start vpnyourtrace.service`

`sudo systemctl status vpnyourtrace.service` 



Source : 

[Installation Openvpn](https://www.cyberciti.biz/faq/howto-setup-openvpn-server-on-ubuntu-linux-14-04-or-16-04-lts/)

[Iptable](https://danielmiessler.com/study/iptables/)

