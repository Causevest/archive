# Author: github.com.prakashpandey

set -ex

# docker hub username
USERNAME=prakashpandey
# image name
IMAGE=tinycoin
sudo docker build --no-cache -t $USERNAME/$IMAGE:latest .