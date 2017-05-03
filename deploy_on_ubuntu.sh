#!/bin/bash -e

# Script variables

GIT_REPO_URL = 'https://github.com/thiezn/nethelper.git'
APP_FOLDER = '/usr/local/nethelper'


# Start deployment

echo 'Script to install and configure nethelper fully on a fresh Ubuntu 16.04 LTS VM on Azure'
echo 'Run as "sudo -H ./deploy_on_ubuntu.sh &> deployment.log"'
echo -e '\n\n============== Updating standard packages ==============\n\n'
apt-get update
apt-get -y upgrade


echo -e '\n\n============== Installing Python Package Manager ==============\n\n'
apt-get -y install python3-pip
pip3 install --upgrade pip


echo -e '\n\n============== Retrieving application ==============\n\n'
mkdir $APP_FOLDER
cd $APP_FOLDER
git clone $GIT_REPO_URL


echo -e '\n\n============== Installing Python3 dependencies ==============\n\n'
pip3 install -r requirements.txt
pip3 install -r optional-requirements.txt


echo -e '\n\n============== Create and use system user for application ==============\n\n'
useradd -r -s /bin/false nethelper
chown -R nethelper:nethelper $APP_FOLDER


echo -e '\n\n============== Configure systemd application service ==============\n\n'
cp $APP_FOLDER/systemd/nethelper.service /lib/systemd/system/
systemctl enable nethelper


echo -e '\n\n============== Launching application ==============\n\n'
cp $APP_FOLDER/config/server.json-sample $APP_FOLDER/config/server.json
systemctl start nethelper
systemctl status nethelper
