FROM ubuntu:latest

# Set non-interactive mode for package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and upgrade packages
RUN apt-get update -y \
    && apt-get update  --fix-missing \
    && apt-get upgrade -y \  
    && apt install -y software-properties-common -y \
    && apt install -y lsb-release gnupg2 ca-certificates apt-transport-https

# Install Apache and PHP and its dependencies
RUN apt-get install -y apache2 \
    git \
    zip \
    wget \
    curl \
    python3 \
    python3-pip \
    vim \
    nano \
    supervisor

RUN python3 -m pip install requests

RUN cd /etc/apache2/mods-enabled && ln -s ../mods-available/cgi.load \
    && /etc/init.d/apache2 restart

# Git clone controleur
COPY ./cgi-bin/* /usr/lib/cgi-bin/
COPY ./src/Controleur/install.sh /root/

#RIGHT MANA
RUN chmod +x /root/install.sh

RUN chmod -R +x /usr/lib/cgi-bin && \
    chown www-data:www-data -R /usr/lib/cgi-bin

#Supervisor
RUN mkdir -p /var/log/supervisor && \
    mkdir -p /var/run/supervisor && \
    chmod 700 /var/log/supervisor && \
    chmod 700 /etc/supervisor && \
    chmod 700 /var/run/supervisor

COPY ./src/supervisor/controleur/supervisord.conf /etc/supervisor/conf.d/

#Apache2 SSL 

COPY ./src/Controleur/000-default.conf /etc/apache2/sites-enabled/

RUN (openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
-subj "/C=FR/ST=SQY/L=SQY/O=YourTrace/CN=controleur" \
-keyout /etc/ssl/private/selfsigned-server.key \
-out /etc/ssl/certs/selfsigned-server.crt) && \
a2enmod ssl

#Cleaning
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/* && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]
