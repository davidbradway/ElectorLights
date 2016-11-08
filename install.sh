#!/bin/bash
clear

echo "Update and install dependencies"
sudo apt-get update -y
sudo apt-get install -y python-pip python-serial python-requests build-essential python-dev git scons swig
pip install requests beautifulsoup4
echo " "

echo "Repo: fetch, compile, and install submodule"
git submodule init
git submodule update
cd rpi_ws281x
scons
cd python
sudo python setup.py install
cd ../..
echo " "

echo "Make script service start at boot"
sudo cp electorlights.sh /etc/init.d/
sudo chmod 755 /etc/init.d/electorlights.sh
sudo update-rc.d electorlights.sh defaults
echo " "

echo "Run a script every minute to check if the processes needs respawned"
long_str="* * * * * $(pwd)/autorestart.sh"
(sudo crontab -l ; echo "$long_str")| sudo crontab -
