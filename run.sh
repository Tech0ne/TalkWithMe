#!/bin/bash

echo "==== Clearing previous image ===="
sudo docker rmi twm_server

echo "==== Building latest image ===="
sudo docker build -t twm_server .

echo "==== Running image ===="
sudo docker run -it --rm --network host \
    -v /var/run/dbus:/var/run/dbus \
    -e DBUS_SESSION_BUS_ADDRESS="unix:path=/var/run/dbus/system_bus_socket" \
    twm_server
