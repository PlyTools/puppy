#!/bin/bash

printHelp () {
	echo "Usage: ./change_network <mode> <arg1> <arg2>"
	echo ""
	echo "    <mode>:"
	echo "          wifi             change to wifi mode to connect wifi"
	echo "          ap               change to ap mode"
	echo "              name         name of ap"
	echo "              passwd       passward of ap"
}

if [ "$1" == "wifi" ]
then
     sudo ifup wlan0
elif [ "$1" == "ap" ]
then
	if [ "$2" == "" ] || [ "$3" == "" ]
	then
		printHelp
	else
		sudo ifdown wlan0
		sudo create_ap --no-virt wlan0 eth0 $2 $3
	fi
else
	printHelp
fi	

