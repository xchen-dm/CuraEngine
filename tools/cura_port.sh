#!/bin/bash
#
# This script grabs the local port of a running Cura instance and outputs the connect string for CuraEngine to prompt
# and clipboard. This allows an IDE such as Clion to always have the correct port number. Simply add the line below to
# the argument in the configuration.
#
# connect $ClipboardContent$ -v
#
# make sure you run this script each time you start the configuration by simply creating an external tool
# Make sure you have xclip installed
#
CURA_CONNECT=$(lsof -i -P -n | grep LISTEN | grep $(ps aux | awk '{ if ($12 ~ "cura_app.py") { print $2 } }') | grep 127.0.0.1 |  awk '{print $9}')
echo $CURA_CONNECT | xclip -rmlastnl -selection clipboard
echo $CURA_CONNECT