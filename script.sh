#!/bin/bash

dir=~

sudo apt-get install tmux

echo 'if ! tmux has-session -t caldera' >> ~/.bashrc
echo 'then' >> ~/.bashrc
echo '\t''tmux new -s caldera -d' >> ~/.bashrc
echo 'tmux send -t caldera "docker run -p 8888:8888  -v '$dir'/arsenal/:/usr/src/app/plugins/arsenal/ -v '$dir'/almanac/:/usr/src/app/plugins/almanac/ -v '$dir'/arsenal/default.yml:/usr/src/app/conf/local.yml butler.mitre.org/atlas/caldera-dev:latest" Enter'  >> ~/.bashrc
echo 'fi' >> ~/.bashrc
