FROM ubuntu:22.04

ENV COMPOSER_ALLOW_SUPERUSER=1

# Set non-interactive mode for package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and upgrade packages
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt install -y software-properties-common -y \
    && apt install -y lsb-release gnupg2 ca-certificates apt-transport-https


#Add Sury php apt repo
RUN add-apt-repository ppa:ondrej/php \
    && apt-get update -y

# Install Apache and PHP and its dependencies
RUN apt-get install -y apache2 \
    php8.3 \
    php8.3-zip \
    php8.3-dev \
    php8.3-mysql \
    libapache2-mod-php \
    php8.3-curl \
    php-json \
    php-xml \
    php8.3-common \
    php8.3-mbstring \
    php-fpm \
    libmcrypt-dev \
    git \
    zip \
    wget \
    curl \
    supervisor \
    php-intl

# Install Composer
RUN curl -sS "https://getcomposer.org/installer" | php -- --install-dir=/usr/local/bin --filename=composer

# Create folder yourtrace
WORKDIR /var/www/html

#Supervisor
RUN mkdir -p /var/log/supervisor && \
    mkdir -p /var/run/supervisor && \
    chmod 700 /var/log/supervisor && \
    chmod 700 /etc/supervisor && \
    chmod 700 /var/run/supervisor

COPY ./infra/YourTrace_Docker/src/supervisor/webserver/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#php fpm
RUN a2enmod proxy_fcgi setenvif
RUN a2enconf php*.*-fpm

# Install symfony (needed to be after)
RUN wget https://get.symfony.com/cli/installer -O - | bash 

RUN mv /root/.symfony5/bin/symfony /usr/local/bin/symfony 

#now
COPY ./website/. /var/www/html/

# Install dependencies
RUN composer install --no-scripts --ignore-platform-req=ext-xml --ignore-platform-req=ext-dom

RUN composer update --no-scripts --ignore-platform-req=ext-xml --ignore-platform-req=ext-dom

EXPOSE 8000 443

# Force cache removal for clean website setup
RUN rm -rf /var/www/html/var/cache

#Cleaning
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/* && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]
