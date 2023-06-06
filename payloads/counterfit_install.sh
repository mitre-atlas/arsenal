#!/bin/bash

if [ ! -d "$HOME/venv/cf_venv" ]; then
	if [ ! -d "$HOME/venv" ]; then
		mkdir $HOME/venv/
	fi
	python3 -m venv $HOME/venv/cf_venv
fi
if ! { $HOME/venv/cf_venv/bin/pip list CounterFit | grep 'CounterFit'; } >/dev/null 2>&1; then
	$HOME/venv/cf_venv/bin/python3 -m pip install -U pip wheel setuptools >/dev/null
	$HOME/venv/cf_venv/bin/python3 -m pip install git+https://github.com/Azure/counterfit.git@main >/dev/null
	$HOME/venv/cf_venv/bin/python3 -m pip install counterfit[dev] >/dev/null
fi



if ! [ -e $HOME/venv/cf_venv/bin/python3 ]; then
	echo "$HOME/venv/cf_venv/bin/python3";
fi
