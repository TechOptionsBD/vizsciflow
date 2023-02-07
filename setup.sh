#!/bin/bash

echo "Installing docker..."

apt-get update -y

apt-get upgrade -y

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

rm -f /usr/share/keyrings/docker-archive-keyring.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install -y docker-ce docker-ce-cli containerd.io

echo "Starting docker..."
sudo service docker start
#sudo service docker status

#docker-compose
echo "Installing docker-compose..."

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Configuring docker for vscode"
sudo usermod -aG docker $USER
sudo apt install -y acl
sudo setfacl --modify user:$USER:rw /var/run/docker.sock

#git clone https://github.com/srlabUsask/vizsciflow.git

#cd vizsciflow

#rm vizsciflow.sql
#wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1HP70Wbnb927iG3hq3Ta01ErR_C65-8Y2' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1HP70Wbnb927iG3hq3Ta01ErR_C65-8Y2" -O vizsciflow.sql && rm -rf /tmp/cookies.txt

#rm -r ./src/plugins/modules
#wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1nFfYaQJTRPDvENVEf8XV23fJqyXN2P1A' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1nFfYaQJTRPDvENVEf8XV23fJqyXN2P1A" -O modules.tar.bz2 && rm -rf /tmp/cookies.txt
#tar -xf modules.tar.bz2 -C ./src/plugins

#sed -i -e "s?/home/vizsciflow/vizsciflow?$(pwd)?" .env
echo "Recreate the dockers ..."
sed -i -e "s/UID=10611135/UID=$(id -u)/" .env
docker-compose down
docker volume prune -f
docker-compose up --build --force-recreate -d

echo "Update database schema and insert default value from vizsciflow.sql ..."
docker cp vizsciflow.sql vizsciflowdb:/
docker exec -i vizsciflowdb psql -U phenodoop -d biowl < vizsciflow.sql

echo "Add modules from src/plugins/modules to the database"
docker exec -i vizsciflowweb sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertmodules --path plugins/modules --with-users False --install-pypi False)'

echo "Add modules from workflows to the database"
docker exec -i vizsciflowweb sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertworkflows --path workflows)'