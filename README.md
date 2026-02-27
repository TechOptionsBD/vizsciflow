# vizsciflow
VizSciFlow is a scientific workflow management system. It provides a domain-specific language (DSL) for specifying the workflow model. Developers need Linux or WSL 2 on Windows to setup the development system locally.

*******
quick install:
- Clone the repository and cd into it. 
- If setup.sh file is not executable (ls -la setup.sh to check), make it executable: chmod +x ./setup.sh
- sudo ./setup.sh
- Continue from step 13 of the following steps.
*******


Step-by-step installation:

1. Install Docker (includes Docker Compose v2) if not already installed:

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker
```

Verify the installation:

```bash
docker --version
docker compose version
```

2. Clone the repository: git clone https://github.com/srlabUsask/vizsciflow.git
3. Delete the src/plugins/modules folder: `rm -r ./src/plugins/modules`
4. Download modules.tar.bz2 from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
5. Extract modules.tar.bz2 to src/plugins: `tar -xf modules.tar.bz2 -C ./src/plugins`
6. Download vizsciflow.sql from this location: https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing
7. Run id command in terminal: `id -u`
8. Set the result to UID in .env file: `UID=10611134`
9. Create the Docker network: `docker network create vizsciflownetwork 2>/dev/null || true`
10. Build and start the containers: `docker compose up -d`
11. Browse localhost:5000. You should see first screen of VizSciFlow.
12. Restore the database: `docker exec -i vizsciflowdb psql -U phenodoop -d biowl < vizsciflow.sql`
13. Browse or reload localhost:5000
14. Log into the system with username: testuser@usask.ca and password: aaa
15. Steps 16-19 are only for those who want the development environment (e.g. tool development) using visual studio code (vscode) IDE.
16. Install "Docker" and "Dev Containers" extensions in vscode. "Docker" tab will appear.
17. Click the "Docker" tab. You will see all docker images and docker containers.
18. Right click on vizsciflowweb docker and click "Attach Visual Studio Code". A new vscode window will appear and it will take several minutes to complete.
19. You are now in full development mode of vizsciflow inside a docker container. You can copy .vscode/launch.json from outside to .vscode/launch.json inside vizsciflowweb and debug.
20. This step is for those who don't use vscode IDE. Without vscode step, you can change code and view the effect, but you can't debug. And if you change .env file, you have to down the docker containers and up again like below:

```bash
docker compose down
docker compose up -d
```
