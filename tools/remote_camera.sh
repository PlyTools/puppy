#!/bin/bash

echo "try push camera stream ......"
echo "You can visit stream at:"
echo "    192.168.3.111:8080/?action=stream"

cd ~/Software/mjpg-streamer/mjpg-streamer-experimental
./mjpg_streamer -i "./input_raspicam.so" -o "./output_http.so -w ./www"
