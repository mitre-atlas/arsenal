#!/bin/bash

shopt -s expand_aliases
alias conda=./miniconda3/bin/conda

# install conda if needed
if [ ! -f "./miniconda3/bin/conda" ]; then
	curl -s https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O
	bash Miniconda3-latest-Linux-x86_64.sh -b
fi

source ./miniconda3/bin/activate
 
# setup conda env if needed
if ! { conda env list | grep 'cfit'; } >/dev/null 2>&1; then
	conda create -y python=3.8 -n cfit > /dev/null
	conda activate cfit
	conda install -c conda-forge gcc
fi

conda activate cfit

# install counterfit if needed
if ! {  pip list counterfit | grep 'counterfit'; } >/dev/null 2>&1; then
	pip install -U pip
	pip install git+https://github.com/Azure/counterfit.git
fi

# call our counterfit script here
python -c "import counterfit; print(counterfit.__path__)"
