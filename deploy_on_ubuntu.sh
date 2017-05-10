#!/bin/bash

# Script variables
GIT_REPO_URL='https://github.com/thiezn/nethelper.git'
APP_BASE_FOLDER='/usr/local'
APP_FOLDER=$APP_BASE_FOLDER'/nethelper'


# Start deployment
echo 'Script to install and configure nethelper fully on a fresh Ubuntu 16.04 LTS VM on Azure'
echo 'Run as "sudo -H ./deploy_on_ubuntu.sh &> install.log &"'
echo -e '\n\n============== Updating standard packages ==============\n\n'
apt-get update
apt-get -f -y upgrade


echo -e '\n\n============== Installing Python Package Manager ==============\n\n'
apt-get -f -y install python3-pip
pip3 install --upgrade pip


echo -e '\n\n============== Retrieving application ==============\n\n'
cd $APP_BASE_FOLDER
git clone $GIT_REPO_URL
cp $APP_FOLDER/config/server.json-sample $APP_FOLDER/config/server.json


echo -e '\n\n============== Installing Python3 dependencies ==============\n\n'
pip3 install -r $APP_FOLDER/requirements.txt
pip3 install -r $APP_FOLDER/optional-requirements.txt

echo -e '\n\n============== Generate self-signed certificate ==============\n\n'
mkdir /etc/ssl/nethelper/
cd /etc/ssl/nethelper/
openssl req -subj "/CN=mortimer.trafficmanager.net/O=NetHelper/C=NL" -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout nethelper.key -out nethelper.crt
chown -R root:root /etc/ssl/nethelper
cd $APP_BASE_FOLDER

echo -e '\n\n============== Create and use system user for application ==============\n\n'
useradd -r -s /bin/false nethelper
chown -R nethelper:nethelper $APP_FOLDER


echo -e '\n\n============== Installing and configuring ngnix ==============\n\n'
apt-get -f -y install nginx-full
rm -fv /etc/nginx/sites-enabled/default
cp $APP_FOLDER/nginx/nethelper.conf /etc/nginx/sites-enabled/
systemctl restart nginx
systemctl status nginx


echo -e '\n\n============== Configure systemd application service ==============\n\n'
cp $APP_FOLDER/systemd/nethelper.service /lib/systemd/system/
systemctl enable nethelper


echo -e '\n\n============== Launching application ==============\n\n'
systemctl start nethelper
systemctl status nethelper
