#!/bin/bash

dir=~

# update container and install a gnome-terminal
# sudo apt-get update
# sudo apt-get install gnome-terminal
# sudo python3 -m pip install --upgrade pip

# clone almanac
cd ~/almanac git pull || git clone https://gitlab.mitre.org/advml/almanac.git

# clone caldera
cd ~/caldera && git checkout tags/4.1.0 || git clone https://github.com/mitre/caldera.git --recursive
cd ~/caldera 
pip3 install -r requirements.txt && cd ~

# clone ml-vulhub
cd ~/ml-vulhub git pull && cd ~ || git clone https://gitlab.mitre.org/advml/ml-vulhub.git

# automate launching ml-vulhub docker images -- port specified by example docker-compose file
gnome-terminal --tab -- bash -c "cd ~/ml-vulhub/envs/example-00-ml-dev/ && ~./init.sh && docker-compose up &"

# put `arsenal` and `almanac` in `caldera` plugins dir via symlink
ln -s ./arsenal ~/caldera/plugins/
ln -s ./arsenal/default.yml ~/caldera/conf/local.yml
ln -s ./almanac ~/caldera/plugins/

# start server.py
gnome-terminal --tab -- bash -c "cd ~/caldera && python3 server.py --insecure"




