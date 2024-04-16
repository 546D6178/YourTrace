FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y software-properties-common

RUN LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/php

RUN apt-get update -y && apt-get install -y  apache2 php8.2 apache2 mariadb-server php8.2-dev php8.2-mysql libapache2-mod-php8.2 php8.2-curl php-json php8.2-common php8.2-mbstring composer git libmcrypt-dev vim nano

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN curl -s "https://packagecloud.io/install/repositories/phalcon/stable/script.deb.sh" | /bin/bash

RUN rm -rfv /etc/apache2/sites-enabled/*.conf

RUN ln -s /etc/apache2/sites-available/slc.conf /etc/apache2/sites-enabled/slc.conf

WORKDIR /var/www/html

CMD ["apachectl","-D","FOREGROUND"]

RUN a2enmod rewrite

EXPOSE 80 443
