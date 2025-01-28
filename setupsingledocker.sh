#!/bin/bash

echo "Installing docker..."

sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install -y docker-ce docker-ce-cli containerd.io

echo "Starting docker..."
sudo service docker start
#sudo service docker status

echo "Configuring docker for vscode"
sudo usermod -aG docker $USER
sudo apt install -y acl
sudo setfacl --modify user:$USER:rw /var/run/docker.sock

echo "Delete old container and docker image ..."
docker container stop vizsciflowfull
docker container rm vizsciflowfull
docker image rm vizsciflowfull

#git clone https://github.com/srlabUsask/vizsciflow.git
#cd vizsciflow

echo "Download default tools"
echo "Delete the src/plugins/modules folder"
[[ -d ./src/plugins/modules ]] && sudo rm -fr ./src/plugins/modules
echo "Downloading modules.tar.bz2 from https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing"
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1nFfYaQJTRPDvENVEf8XV23fJqyXN2P1A' -O modules.tar.bz2
echo "Extracting modules.tar.bz2 to src/plugins..."
sudo tar -xf modules.tar.bz2 -C ./src/plugins

echo "Download templates and saved workflows"
if [ -f ./workflows ]; then
    sudo rm -f ./workflows
fi
echo "Downloading workflows from https://docs.google.com/document/d/1Kg5yCnhVb0QNIyqDmjNQWXICqPzUdoXL4PgtCz7F6BU/edit?usp=sharing"
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Kg5yCnhVb0QNIyqDmjNQWXICqPzUdoXL4PgtCz7F6BU' -O workflows

# build docker image
docker build --build-arg UID=`id -u` -t vizsciflowfull:latest .
docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull:latest

docker exec vizsciflowfull sh -c "/home/vizsciflow/wait_for_pg_ready.sh"
docker exec vizsciflowfull sh -c "PGPASSWORD='sr-hadoop' psql -U phenodoop -d biowl -f /home/vizsciflow/vizsciflow.sql"
echo "Add modules from src/plugins/modules to the database"
docker exec -i vizsciflowfull sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertmodules --path /home/vizsciflow/src/plugins/modules --with-users False --install-pypi False)'

echo "Add workflows from src/plugins/modules to the database"
docker exec -i vizsciflowfull sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertworkflows --path /home/vizsciflow/workflows)'

docker commit vizsciflowfull vizsciflowfull:latest
docker save vizsciflowfull:latest > vizsciflowfull.tar