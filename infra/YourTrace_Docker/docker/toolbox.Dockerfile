FROM ubuntu:latest

# Set non-interactive mode for package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and upgrade packages
RUN apt-get update -y \
    && apt-get update  --fix-missing \
    && apt-get upgrade -y \  
    && apt install -y software-properties-common -y \
    && apt install -y lsb-release gnupg2 ca-certificates apt-transport-https

# Install paquets and dependencies
RUN apt-get install -y apache2 \
    git \
    zip \
    wget \
    curl \
    python3 \
    python3-pip \
    nano \
    vim \
    supervisor 

RUN apt install -y jq


RUN python3 -m pip install requests \
    && python3 -m pip install beautifulsoup4 \
    && python3 -m pip install selenium \
    && python3 -m pip install pandas \
    && python3 -m pip install regex \
    && python3 -m pip install webdriver-manager \
    && python3 -m pip install undetected-chromedriver 

#Ignorant

RUN pip3 install ignorant

#Maigret

#RUN pip3 install maigret
RUN git clone https://github.com/soxoj/maigret.git && \
    cd maigret && pip3 install -r requirements.txt && \
    python3 setup.py build && python3 setup.py install
    
RUN pip install typing_extensions==4.9.0 --upgrade

#Holehe

RUN pip3 install holehe



#h8mail

RUN pip3 install h8mail


# Create folder yourtrace
#WORKDIR /var/www/html

RUN cd /etc/apache2/mods-enabled && ln -s ../mods-available/cgi.load \
    && /etc/init.d/apache2 restart

# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

#Add src File
COPY ./cgi-bin/ /usr/lib/cgi-bin/
ADD ./src/Toolbox/chromium.sh /root/
ADD ./src/Toolbox/install.sh /root/


#RIGHT MANAGEMENT
RUN chmod +x /root/install.sh /root/chromium.sh

RUN chmod -R +x /usr/lib/cgi-bin && \
    chown www-data:www-data -R /usr/lib/cgi-bin

RUN mkdir /var/www/html/result && \
    chown www-data:www-data /var/www/html/result

RUN chown -R www-data:www-data /var/www/

RUN groupadd cgi-bin && \
    usermod -aG cgi-bin www-data && usermod -aG cgi-bin root && \
    chown -R root:cgi-bin /usr/local/lib/python3.10/dist-packages/

#Supervisor
RUN mkdir -p /var/log/supervisor && \
    mkdir -p /var/run/supervisor && \
    chmod 700 /var/log/supervisor && \
    chmod 700 /etc/supervisor && \
    chmod 700 /var/run/supervisor

COPY ./src/supervisor/toolbox/supervisord.conf /etc/supervisor/conf.d/

#Apache2 SSL 

COPY ./src/Toolbox/000-default.conf /etc/apache2/sites-enabled/

RUN (openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
-subj "/C=FR/ST=SQY/L=SQY/O=YourTrace/CN=toolbox" \
-keyout /etc/ssl/private/selfsigned-server.key \
-out /etc/ssl/certs/selfsigned-server.crt) && \
a2enmod ssl 

#cleaning
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/* && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]
