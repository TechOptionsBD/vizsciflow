# vizsciflow
VizSciFlow is a scientific workflow management system. It provides a domain-specific language (DSL) for specifying the workflow model. Developers need Linux or WSL 2 on Windows to setup the development system locally.

1. Install docker if it is not already installed using https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 or follow these steps below:

apt-get update -y

apt-get upgrade -y

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y

sudo apt-get install -y docker-ce docker-ce-cli containerd.io

sudo service docker status

#docker-compose

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

2. Clone the repository: git clone https://github.com/srlabUsask/vizsciflow.git
3. cd into the folder: cd vizsciflow and change the basedir to your vizsciflow folder and DATA_DIR to its storage subfolder.
4. Delete vizsciflow.sql file.
5. Download vizsciflow.sql file into vizsciflow folder from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
6. Delete the src/plugins/modules folder: rm -r ./src/plugins/modules
7. Download modules.tar.bz2 from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
8. Extract modules.tar.bz2 to src/plugins: tar -xf modules.tar.bz2 -C ./src/plugins
9. Run id command in terminal: id
10. Use the uid from id command's output and replace UID in .env file with it.
11. Build the docker: sudo docker-compose up -d
12. Browse localhost:5000. You should see first screen of VizSciFlow.
13. Copy vizsciflow.sql file to vizsciflowdb docker: docker cp vizsciflow.sql vizsciflowdb:/
14. Shell into the vizsciflowdb docker. docker exec -it vizsciflowdb /bin/bash
15. Restore the database from vizsciflow.sql inside vizsciflowdb shell:  psql -U phenodoop -d biowl < vizsciflow.sql
16. Log into the system with username: testuser@usask.ca and password: aaa
17. Browse or reload localhost:5000

Steps 18-21 are only for those who use visual studio code (vscode) IDE.
18. Install "Docker" extension in vscode. "Docker" tab will appear.
19. Click the "Docker" tab. You will see all docker images and docker containers.
20. Right click on vizsciflowweb docker and click "Attach Visual Studio Code". A new vscode window will appear and it will take several minutes to complete.
21. You are now full development mode of vizsciflow inside a docker container. You can copy .vscode/launch.json from outside to .vscode/launch.json inside vizsciflowweb and debug.
22. This step is for those who don't use vscode IDE. Without vscode step, you can change code and view the effect, but you can't debug. And if you change .env file, you have to down the docker containers and up again like below:
docker-compose down
docker-compose up -d
