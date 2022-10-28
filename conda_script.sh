#!/bin/bash

dir=~

# clone almanac
git clone https://gitlab.mitre.org/advml/almanac.git

# clone caldera
git clone https://github.com/mitre/caldera.git

# clone ml-vulhub
git clone https://gitlab.mitre.org/advml/ml-vulhub.git

# automate launching ml-vulhub docker images -- port specified by example docker-compose file
cd ml-vulhub/envs/example-00-ml-dev
./init.sh
docker-compose up

# put `arsenal` and `almanac` in `caldera` plugins dir via symlink
ln -s ./arsenal ~/caldera/plugins/
ln -s ./almanac ~/caldera/plugins/
ln -s ./arsenal/default.yml ~/caldera/conf/local.yml

# start server.py
cd caldera
python3 server.py




