#!/bin/bash

# Define environment variables
HOST="http://127.0.0.1"
PORT=5000
PEERS="http://127.0.0.1:5001"
MINER_ADDRESS="ppdpp-dvfgf-fredgdsdf-gdsfgsd-35vr433-ee2eass4d"

# Export environment variables
echo "Exporting HOST=$HOST"
export HOST=$HOST
echo "Exporting PORT=$PORT"
export PORT=$PORT
echo "Exporting PEERS=$PEERS"
export PEERS=$PEERS
echo "Exporting MINER_ADDRESS=$MINER_ADDRESS"
export MINER_ADDRESS=$MINER_ADDRESS

# Start application
echo "Starting application.... "
python src/app.py