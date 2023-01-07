# vizsciflow
VizSciFlow is a scientific workflow management system. It provides a domain-specific language (DSL) for specifying the workflow model.

Developers can follow the below steps to deploy it in local system.

1. Install docker if it is not already installed using https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 or follow these steps below:

apt-get update -y

apt-get upgrade -y

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install -y docker-ce docker-ce-cli containerd.io

#docker-compose

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

2. Clone the repository: git clone https://github.com/srlabUsask/vizsciflow.git
3. cd into the folder: cd vizsciflow
4. Delete the src/plugins/modules folder: rm -r ./src/plugins/modules
5. Download modules.tar.bz2 from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
6. Remove ./src/plugins/modules folder. rm -r ./src/plugins/modules
7. Extract modules.tar.bz2 to src/plugins: tar -xf modules.tar.bz2 -C ./src/plugins
8. Run id command in terminal: id
9. Use the uid from id command's output and replace UID in .env file with it.
10. Build the docker: sudo docker-compose up -d
11. Browse localhost:5000. You should see first screen of VizSciFlow.
12. Delete vizsciflow.sql file.
13. Download vizsciflow.sql file from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
14. Copy vizsciflow.sql file to vizsciflowdb docker: docker cp vizsciflow.sql vizsciflowdb:/
15. Shell into the vizsciflowdb docker. docker exec -it vizsciflowdb /bin/bash
16. Restore the database from vizsciflow.sql inside vizsciflowdb shell:  pg_restore -U postgres -d biowl vizsciflow.sql
17. Log into the system with username: testuser@usask.ca and password: aaa
18. Browse or reload localhost:5000
19. Install "Docker" extension in vscode. "Docker" tab will appear.
20. Click the "Docker" tab. You will see all docker images and docker containers.
21. Right click on vizsciflowweb docker and click "Attach Visual Studio Code". A new vscode window will appear and it will take several minutes to complete.
22. You are now full development mode of vizsciflow inside a docker container. You can copy .vscode/launch.json from outside to .vscode/launch.json inside vizsciflowweb and debug.
