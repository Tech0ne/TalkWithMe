#!/bin/bash

if [[ "$(id -u)" -ne 0 ]]; then
    echo "Please run as root"
    exit 1
fi

install_dir="/opt/twm_server/"

if [ -d "$install_dir" ]; then
	echo "$install_dir already exists."
    echo "Press Ctrl+C if you want to stop, or press enter to continue"
    read
fi

mkdir "$install_dir"

cp ./Dockerfile "$install_dir"
cp ./run.sh "$install_dir"
cp ./server.py "$install_dir"
cp ./icon.png "$install_dir"