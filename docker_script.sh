#!/bin/bash

dir=~

sudo apt-get update
sudo apt-get install gnome-terminal
sudo apt-get install tmux
sudo apt-get install gcc

# clone almanac
cd ~ && git clone https://gitlab.mitre.org/advml/almanac.git

# clone caldera
cd ~ && git clone https://github.com/mitre/caldera.git --recursive
docker-compose up

# # clone ml-vulhub
cd ~ && git clone https://gitlab.mitre.org/advml/ml-vulhub.git

# automate launching ml-vulhub docker images -- port specified by example docker-compose file
# make sure you are added to the `sudo` user group for docker
if ! tmux has-session -t ml_vulhub
then
    tmux new-session -d -s ml_vulhub
    tmux send -t ml_vulhub "cd ~/ml-vulhub/envs/example-00-ml-dev/" ENTER
    tmux send -t ml_vulhub "./init.sh" ENTER
    tmux send -t ml_vulhub "docker-compose up" ENTER  
fi
tmux send -t ml_vulhub "cd ~/ml-vulhub/envs/example-00-ml-dev/" ENTER
tmux send -t ml_vulhub "./init.sh" ENTER
tmux send -t ml_vulhub "docker-compose up" ENTER

# # start server.py
if ! tmux has-session -t caldera
then
    tmux new-session -d -s caldera
    tmux send -t caldera "docker run -p 8888:8888  -v '$dir'/arsenal/:/usr/src/app/plugins/arsenal/ -v '$dir'/almanac/:/usr/src/app/plugins/almanac/ -v '$dir'/arsenal/default.yml:/usr/src/app/conf/local.yml caldera:latest" ENTER  
fi
tmux send -t caldera "docker run -p 8888:8888  -v '$dir'/arsenal/:/usr/src/app/plugins/arsenal/ -v '$dir'/almanac/:/usr/src/app/plugins/almanac/ -v '$dir'/arsenal/default.yml:/usr/src/app/conf/local.yml caldera:latest" ENTER

