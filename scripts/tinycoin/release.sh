# Author: github.com.prakashpandey

set -ex

# docker hub username
USERNAME=prakashpandey
# image name
IMAGE=tinycoin
# ensure we're up to date
git pull

# bump version
# sudo docker run --rm -v "$PWD":/home/tinycoin prakashpandey/tinycoin patch
version=`cat VERSION`
echo "version: $version"
# run build
./build.sh


# use this if you are not using manual commit
# git add -A
# git commit -m "version $version"

# git tag the latest version
git tag -a "$version" -m "version $version"
git push
git push --tags

# tag images
sudo docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$version
# push docker images(optional)
sudo docker push $USERNAME/$IMAGE:latest 
sudo docker push $USERNAME/$IMAGE:$version
