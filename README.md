# vizsciflow
VizSciFlow is a scientific workflow management system. It provides a domain-specific language (DSL) for specifying the workflow model. Developers need Linux or WSL 2 on Windows to setup the development system locally.

*******
quick install:
- Clone the repository and cd into it. 
- If setup.sh file is not executable, make it executable: chmod +x ./setup.sh
- sudo ./setup.sh
- Continue from step 15 of the following steps.
*******


Step-by-step installation:

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
3. Delete vizsciflow.sql file.
4. Download vizsciflow.sql file into vizsciflow folder from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
5. Delete the src/plugins/modules folder: rm -r ./src/plugins/modules
6. Download modules.tar.bz2 from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
7. Extract modules.tar.bz2 to src/plugins: tar -xf modules.tar.bz2 -C ./src/plugins
8. Run id command in terminal: id -u
9. Set the result to UID in .env file: UID=10611134
10. Build the docker: sudo docker-compose up -d
11. Browse localhost:5000. You should see first screen of VizSciFlow.
12. Copy vizsciflow.sql file to vizsciflowdb docker: docker cp vizsciflow.sql vizsciflowdb:/
13. Shell into the vizsciflowdb docker. docker exec -it vizsciflowdb /bin/bash
14. Restore the database from vizsciflow.sql inside vizsciflowdb shell:  psql -U phenodoop -d biowl < vizsciflow.sql
15. Browse or reload localhost:5000
16. Log into the system with username: testuser@usask.ca and password: aaa
17. Steps 18-21 are only for those who use visual studio code (vscode) IDE. 
18. Install "Docker" and "Dev Containers" extensions in vscode. "Docker" tab will appear.
19. Click the "Docker" tab. You will see all docker images and docker containers.
20. Right click on vizsciflowweb docker and click "Attach Visual Studio Code". A new vscode window will appear and it will take several minutes to complete.
21. You are now in full development mode of vizsciflow inside a docker container. You can copy .vscode/launch.json from outside to .vscode/launch.json inside vizsciflowweb and debug.
22. This step is for those who don't use vscode IDE. Without vscode step, you can change code and view the effect, but you can't debug. And if you change .env file, you have to down the docker containers and up again like below:

docker-compose down

docker-compose up -d
