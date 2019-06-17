#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget libsqlite3-dev
sudo wget -P ~ "https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz"
sudo tar xzf ~/Python-3.7.3.tgz -C ~
cd ~/Python-3.7.3/
sudo ./configure --enable-optimizations --enable-loadable-sqlite-extensions && sudo make && sudo make install
#sudo ./configure --enable-loadable-sqlite-extensions && make && sudo make install
cd ~
sudo rm ~/Python-3.7.3.tgz
sudo rm -rf ~/Python-3.7.3/