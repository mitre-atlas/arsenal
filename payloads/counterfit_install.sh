#!/bin/bash

if [ ! -d "$HOME/venv/cf_venv" ]; then
	if [ ! -d "$HOME/venv" ]; then
		mkdir $HOME/venv/
	fi
	python -m venv $HOME/venv/cf_venv
fi

if ! { $HOME/venv/cf_venv/bin/pip list counterfit | grep 'counterfit'; } >/dev/null 2>&1; then
	$HOME/venv/cf_venv/bin/python -m pip install -U pip wheel setuptools >/dev/null
	$HOME/venv/cf_venv/bin/python -m pip install git+https://github.com/Azure/counterfit.git >/dev/null
fi

if [ -e $HOME/venv/cf_venv/bin/python ]; then
	echo "$HOME/venv/cf_venv/bin/python";
fi
