#!/bin/bash
set -e

echo "Installing Docker..."
curl -fsSL https://get.docker.com | sudo sh

echo "Configuring Docker for current user..."
sudo usermod -aG docker $USER
sudo apt-get install -y acl
sudo setfacl --modify user:$USER:rw /var/run/docker.sock

echo "Verifying Docker installation..."
docker --version
docker compose version

echo "Recreating containers..."
sed -i -e "s/^UID=.*/UID=$(id -u)/" .env
docker network create vizsciflownetwork 2>/dev/null || true
docker compose down
docker volume prune -f
docker compose up --build --force-recreate -d

echo "Updating database schema from vizsciflow.sql..."
docker cp vizsciflow.sql vizsciflowdb:/
docker exec -i vizsciflowdb psql -U phenodoop -d biowl < vizsciflow.sql

echo "Adding modules from src/plugins/modules to the database..."
docker exec -i vizsciflowweb sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertmodules --path plugins/modules --with-users False --install-pypi False)'

echo "Adding workflows to the database..."
docker exec -i vizsciflowweb sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertworkflows --path workflows)'

echo "Setup complete. Browse http://localhost:5000"
