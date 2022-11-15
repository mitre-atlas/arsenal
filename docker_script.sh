#!/bin/bash

dir=~

sudo apt-get install tmux

# clone caldera
git clone https://github.com/mitre/caldera.git --recursive || cd ~/caldera || git checkout tags/4.1.0
docker-compose up

# clone almanac
git clone https://gitlab.mitre.org/advml/almanac.git

# clone ml-vulhub
git clone https://gitlab.mitre.org/advml/ml-vulhub.git


# automate launching caldera+arsenal+almanac in a tmux session for development
echo 'if ! tmux has-session -t caldera' >> ~/.bashrc
echo 'then' >> ~/.bashrc
echo '\t''tmux new -s caldera -d' >> ~/.bashrc
echo 'tmux send -t caldera "docker run -p 8888:8888  -v '$dir'/arsenal/:/usr/src/app/plugins/arsenal/ -v '$dir'/almanac/:/usr/src/app/plugins/almanac/ -v '$dir'/arsenal/default.yml:/usr/src/app/conf/local.yml caldera:latest" Enter'  >> ~/.bashrc
echo 'fi' >> ~/.bashrc

# automate launching ml-vulhub docker images -- port is specified by docker-compose file
cd ml-vulhub/envs/example-00-ml-dev
./init.sh
docker-compose up

