apt-get update -y
apt-get upgrade -y

sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

if [ ! -e /usr/share/keyrings/docker-archive-keyring.gpg]
then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg    
fi

echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

#docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# get scidatamanager
apt-get install -y git
# cd /home/vagrant
git pull https://$1:$2@github.com/srlabUsask/vizsciflow.git
#mkdir ../postgres_data/
#cp /vagrant_data/vizsciflow.sql ./postgres_data/

#docker build -t vizsciflow:latest .
#docker run --name vizsciflow -d -p 8000:5000 --rm vizsciflow:latest
/usr/local/bin/docker-compose down
/usr/local/bin/docker-compose build
/usr/local/bin/docker-compose up -d

#docker-compose exec -T db psql -U phenodoop --dbname=biowl -f /var/lib/postgresql/data/vizsciflow.sql
docker-compose exec -T vizsciflowweb .venv/bin/python manage.py createdb
docker-compose exec -T vizsciflowweb .venv/bin/python manage.py deploydb
