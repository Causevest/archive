# Testing script can be used to deploy multiple nodes on same machine in different ports

# Node 1
# PORT=5000
# PEERS="http://127.0.0.1:5001"
# MINER_ADDRESS="ppdpp-dvfgf-fredgdsdf-gdsfgsd-35vr433-ee2eass4d"

# Node 2
# PORT=5001
# PEERS="http://127.0.0.1:5002"
# MINER_ADDRESS="ppdpp-dvfgf-fredgdsdf-gdsfgsd-35vr433-ee2eass4e"

# Node 3
PORT=5002
PEERS="http://127.0.0.1:5000"
MINER_ADDRESS="ppdpp-dvfgf-fredgdsdf-gdsfgsd-35vr433-ee2eass4f"

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