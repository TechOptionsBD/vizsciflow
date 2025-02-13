# A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0 (Artifact)
This document contains the instructions for the SEIS-ICSE 2025 artifact evaluation for paper *A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0*. This paper proposes a novel framework for the cross-domain computational scientific experiment in the context of Society 5.0 and develops a proof-of-concept prototype of a scientific workflow management system (SWfMS) based on the proposed framework. Researchers from different scientific domains can use this multi-user, web-based system to design and execute interdisciplinary workflows collaboratively. This document provides instructions to reproduce the experiments (Section IV) reported in the paper. It is also available online at [BioSocSys GitHub Repository](https://github.com/TechOptionsBD/vizsciflow/blob/vizsciflowdockfull/README.md). This artifact uses the **vizsciflowdockfull** branch of the repository.

Authors: Muhammad Mainul Hossain, Banani Roy, Chanchal Roy, Kevin Schneider

<!-- TOC -->

- [Framework for Cross-Domain Collaborative Scientific Experiments Artifact](#framework-for-cross-domain-collaborative-scientific-experiments-artifact)
  - [Preparing the artifact](#preparing-the-artifact)
  - [Making the artifact available](#making-the-artifact-available)
  - [Documenting the artifact](#documenting-the-artifact)
    - [Purpose](#purpose)
      - [Badges Applying For](#badges-applying-for)
    - [Provenance](#provenance)
      - [Start the Docker Container](#start-the-docker-container)
      - [Build the Docker Image](#build-the-docker-image)
    - [Setup](#setup)
      - [Hardware Requirements](#hardware-requirements)
      - [Software Dependencies](#software-dependencies)
      - [Directory Structure](#directory-structure)
    - [Usage](#usage)
      - [Create a bioinformatics workflow](#create-a-bioinformatics-workflow)
        - [Show prospective provenance](#show-prospective-provenance)
        - [Show Retrospective provenance](#show-retrospective-provenance)
      - [Cross-domain workflows](#cross-domain-workflows)
      - [Tool Integration](#tool-integration)
  - [Submitting the artifact](#submitting-the-artifact)
  - [Conclusion](#conclusion)

<!-- /TOC -->

# Framework for Cross-Domain Collaborative Scientific Experiments Artifact
The convergence of technology and human creativity in Society 5.0 necessitates innovative approaches to tackling complex scientific challenges across diverse domains, making cohesive experimentation essential. Computational scientific experiments employ various methods such as data acquisition, preprocessing, analysis, and visualization to simulate and understand intricate phenomena. However, existing interactive environments often lack the usability and flexibility needed to accommodate researchers of varying skill levels and to support effective cross-domain collaboration.

To address these challenges, we developed a prototype scientific workflow management system (SWfMS) for code clone analysis, bioinformatics, image processing, and machine learning by integrating tools and services from their respective domains. This README provides instructions for the ICSE 2025 Artifact Evaluation Track, associated with the paper **A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0**, accepted in the ICSE 2025 SEIS Track. It includes steps to obtain, install, recreate, and exercise the developed SWfMS.

A scientific workflow integrates software tools and data into a cohesive pipeline for conducting computational scientific experiments. These tools typically involve data transformation or data analysis algorithms. In the following figure, input and output data are interconnected using *tools A...E* tools. During execution, these tools perform specific tasks of the scientific experiment.

![Workflow interconnects tools and data](workflow.svg?raw=true "Workflow Example")

This artifact offers a web-based rapid development interface for intuitively defining experiment logic. Researchers can drag graphical workflow elements, such as datasets, tools, and workflow templates, from the user interface and drop into the code editor. The interface transforms these elements into **Domain-Specific Language (DSL)** code snippets, creating a pipeline for the experiment hypothesis. Researchers can quickly switch to the **control flow graph (CFG)** view for more efficient graphical exploration and comprehension of the workflows. The system facilitates seamless tool integration by end-users, ensuring flexibility and extensibility.  Throughout the experiment lifecycle, the system captures provenance information, including logs, histories, data lineage, and process information. This provenance data is then used to reproduce the experiment and validate the hypothesis.  Researchers can write queries and visualize results through the artifact's intuitive user interface.  Finally, the system offers a robust, efficient, and scalable runtime platform for managing the data and processes.

## Preparing the artifact
The artifact is prepared as a pre-built Docker image, which includes all necessary dependencies and third-party tools. Users can run this Docker image on **Ubuntu 20.04+** (also compatible with **Windows 11 WSL**). Follow these steps to get started:

1. Download vizsciflowfull.tar from https://dx.doi.org/10.6084/m9.figshare.28224869 (DOI: 10.6084/m9.figshare.28224869).
2. Run the following command to load the image from the .tar file (note that you may need *root privileges* to run docker):

```
$ docker load -i vizsciflowfull.tar
```

## Making the artifact available
The artifact is made available through Figshare, a long-term data archival repository. A DOI, 10.6084/m9.figshare.28224869, has been generated for it. The artifact can be downloaded from [Figshare link](https://dx.doi.org/10.6084/m9.figshare.28224869).

## Documenting the artifact
This README document provides comprehensive instructions on the purpose, provenance, data, setup, and usage of the artifact. You can access this file online at: [GitHub Repository](https://github.com/TechOptionsBD/vizsciflow/blob/vizsciflowdockfull/README.md). A separate LICENSE file is also submitted with the uploaded package.

## Purpose
The artifact is a proof-of-concept implementation of a scientific workflow management system (SWfMS) designed for cross-domain collaborative scientific experiments. It features an intuitive web interface that allows researchers to design scientific workflows using a domain-specific language (DSL). Visual support tools and secondary notation facilitate quick workflow code generation. Users can drag and drop workflow artifacts — such as datasets, tools, templates, and histories — presented as graphical elements into the code editor, which then generates the corresponding code snippets. Additionally, a control flow graph provides a quick overview of the workflow.

### Badges Applying For

1. **Available** (Artifact is placed on a publicly accessible archival repository): The artifact is permanently available through Figshare, and a DOI has been created for it. Please check [**Making the artifact available**](#making-the-artifact-available) for details.
2. **Functional** (Artifact is documented, consistent, complete, exercisable, and includes appropriate evidence of verification and validation): This README file provides detailed instructions for installation and describes how to accomplish the exercises outlined in the associated paper. Additionally, once installed, the artifact offers a comprehensive help document detailing installation, language feature, workflow design, tool integration, and so on.
3. **Reusable** (Artifact significantly exceeds minimal functionality): The artifact is well-documented and includes a step-by-step guide for designing workflows and integrating different types of tools. A number of sample workflows are also provided to help users get started. Several scripts are included in the GitHub repository to create this artifact. The datasets necessary to run the workflows shown in the paper are included in the Docker image. Users can also quickly upload new datasets using the *upload feature* of the **Dataset Panel**.

## Provenance
The artifact is available as a pre-built Docker image, containing all dependencies and third-party tools.  Users should have basic familiarity with Docker containerization, including installing Docker on their local system and deploying the artifact as a Docker container. Refer to the [Docker Docs](https://docs.docker.com/get-started/) for information on installing Docker and managing Docker containers. The [Build the Docker Image](#build-the-docker-image) section of this README includes a script with Docker installation instructions. Follow the steps below to start **Docker Engine** and deploy the artifact:

1. Check if Docker is installed:
```
$ docker info
```
You will see information about the **Docker Engine**, if Docker is installed. Otherwise, an error message is shown.
2. Check status and run Docker Engine. In *nix and Mac machines, you can use `service` command if it is available:
```
$ sudo service docker status
# if docker engine is not running, start it
$ sudo service docker start
```
3. Download [vizsciflowfull.tar](https://dx.doi.org/10.6084/m9.figshare.28224869) (DOI: 10.6084/m9.figshare.28224869).
4. Run the following command on it to obtain the Docker image (you may need root privilege to run `docker`):

```
$ docker load -i vizsciflowfull.tar
```

### Start the Docker Container

Follow the below steps to start the Docker container:

1. Run the following command to instantiate the Docker image:

```
$ docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull:latest
```

A Docker container named *vizsciflowfull* will be instantiated.

2. Wait few seconds for service start.
3. Browse to [http://localhost:8000](http://localhost:8000) to access the BioSocSys web interface.
4. Use username *testuser@gmail.com* and password *test2025* to login. 

Once running inside the Docker, you can also find this document at `/home/vizsciflow/README.md`.

### Build the Docker Image

It is **NOT** necessary for the artifact evaluation to rebuild the image, but would be useful for anyone who would like to reuse and access advanced features of BioSocSys.

1. Use the `setupsingledocker.sh` script from [BioSocSys's Github repository](https://github.com/TechOptionsBD/vizsciflow/blob/vizsciflowdockfull) (**vizsciflowdockfull** branch) to rebuild the Docker image from scratch on a clean **Ubuntu 20.04+ machine (compatible also with Windows 11 WSL)**.
2. This script can also be found at `/home/vizsciflow/setupsingledocker.sh` inside the running container.

The steps for building the Docker image are outlined in the script below. Read the *echo* commands for details of the steps.

```
echo "clone the BioSocSys branch of GitHub repository and cd into it."
git clone 
cd vizsciflow

echo "Download default tools and untar under ./src/plugins folder"
echo "Delete the ./src/plugins/modules folder"
[[ -d ./src/plugins/modules ]] && sudo rm -fr ./src/plugins/modules
echo "Downloading modules.tar.bz2 from https://drive.google.com/drive/folders/1GWFv_NK7MPAqXO2bInA34vGk-_J4BNUI?usp=sharing"
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1nFfYaQJTRPDvENVEf8XV23fJqyXN2P1A' -O modules.tar.bz2
echo "Extracting modules.tar.bz2 to src/plugins..."
sudo tar -xf modules.tar.bz2 -C ./src/plugins

echo "Build docker image"
docker build --platform=linux/amd64 --build-arg UID=`id -u` -t vizsciflowfull:latest .
echo "Run the docker image as vizsciflowfull container"
docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull:latest

echo "Waiting for PostgreSQL to finish start."
docker exec vizsciflowfull sh -c "/home/vizsciflow/wait_for_pg_ready.sh"

echo "Inserting the default values in the database ..."
docker exec vizsciflowfull sh -c "PGPASSWORD='sr-hadoop' psql -U phenodoop -d biowl -f /home/vizsciflow/vizsciflow.sql"

echo "Adding modules from ./src/plugins/modules to the database"
docker exec -i vizsciflowfull sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertmodules --path /home/vizsciflow/src/plugins/modules --with-users False --install-pypi False)'

echo "Commiting the changes of vizsciflowfull container into vizsciflowfull image."
docker commit vizsciflowfull vizsciflowfull:latest
echo "Saving the image in .tar file"
docker save vizsciflowfull:latest > vizsciflowfull.tar
```

## Setup
### Hardware Requirements
The artifact supports x86-64 architecture running Linux-based operating systems. It is also compatible with Windows 11 WSL. The NiCad workflow experiment results reported in the paper (TABLE II) is obtained from a machine with 12 physical cores and 16 GB of memory. Different hardware environment may result in numbers with different characteristics, but we expect the trend and ratio to be similar.

### Software Dependencies
The Docker image runs Debian GNU/Linux 11 (bullseye), built from the python:3.10-bullseye DockerHub image. It implements cross-domain BioSocSys Scientific Workflow Management System (SWfMS) and integrates tools for code clone detection, bioinformatics, machine learning, and image processing. To minimize the Docker image size, we installed only the essential tools required to perform the experiments described in the paper.


The Docker image contains the following software dependencies:
- Python 10.0
- PostgreSQL 13.4
- Flask 2.0.1
- Java Virtual Machine 11.0.11

Tools integrated in the SWfMS:
- FastQC
- BWA-MEM
- PEAR
- NiCad
- Python packages for machine learning and image processing, for example, 
  - opencv-python
  - scikit-image
  - pandas
  - numpy
  - biopython
  - scikit-learn
  - scipy
  - joblib

### Directory Structure

We briefly describe the organization of BioSocSys's code base, located at /home of the Docker image:
- 'venvs/' contains the virtual environments for the system and tools
- 'vizsciflow/' contains all files of the system
  - 'storage/' contains the files/folders of the data
  - 'vizsciflow.log' is the log file of the system
  - 'src' contains the source code of the SWfMS
    - 'app/' contains the main code of the system
        - 'static/' contains the static files of the system
        - 'templates/' contains the HTML templates of the system
        - 'main/' contains the main code of the backend
            - 'views.py' contains the views of the system
            - 'jobsviews.py' contains the views of the running jobs
            - 'forms.py' contains the forms of the system
            - 'chat.py' contains the chat code of the system
            - 'errors.py' contains the error handling code of frequent HTTP errors
        - 'utils.py' contains the utility functions of the system
        - 'managers/' contains the managers of the system
            - 'usermgr.py' contains the user manager of the system
            - 'workflowmgr.py' contains the workflow manager of the system
            - 'toolmanager.py' contains the tool manager of the system
            - 'chatmgr.py' contains the chat manager of the system
            - 'activitymgr.py' contains the activity manager of the system
            - 'dbmgr.py' contains the database manager of the system
            - 'datamgr.py' contains the data manager of the system
            - 'mgrutil' contains the utility functions of the managers
            - 'runmgr.py' contains the run manager of the system
            - 'filtermgr.py' contains the filter manager of the system
            - 'modulemgr.py' contains the module manager of the system
            - 'wrappers/' contains the wrappers of the system
                - 'db.py' contains the database wrapper of the system
                - 'graph.py' contains the neo4j graph wrapper of the system
            - 'objectmodel/' contains the object models of the system
                - 'common.py' contains the common object model of the system
                - 'models/' contains the models of the system
                    - 'rdb.py' contains the relational database models of the system
                    - $'new4j_graphutils.py'$ contains the neo4j graph models of the system
                    - $'py2neo\_graphutils.py'$ contains the py2neo graph models of the system
                    - 'loader.py' contains data and module loaders of the system
    - 'plugins':
        - 'modules': tool and provenance capture plugins
        - 'provs': provenance query plugins
    - 'config.py' is the configuration file of the system
    - 'manage.py' is the script to run the system
    - 'migrations/' contains the database migration files
    - 'requirements/' contains the dependencies of the Python system
    - 'tests/' contains the test files of the system
    - 'run.sh' is the script to run the system

## Usage

### Create a bioinformatics workflow

Follow the steps below to create a bioinformatics workflow using the BioSocSys SWfMS:

1. Open a web browser and navigate to [http://localhost:8000](http://localhost:8000).
2. Log in using the username: **testuser@gmail.com** and password: **test2025**.
3. Expand **Dataset Panel** to **LocalFS/public/MiSeq_SOP/** and double click on **F3D3_S191_L001_R1_001.fastq**. Following code snippet will be added to the code editor.
```
data = '/public/bio/MiSeqSOPData/F3D3_S191_L001_R1_001.fastq'
```
4. Expand **Dataset Panel** to **LocalFS/public/genomes** and double click on **Chr1.cdna**. Rename the data item to **ref** in the code editor.
5. Search the CheckQuality (fastqc) service in **Services** panel and drag it to the code editor.
6. Search the Align (bwa) service in **Services** panel and drag it to the code editor.
7. Steps 3-7 creates the following lines in the code editor.

```
data = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
ref = '/public/genomes/Chr1.cdna'
html,zip = fastqc.CheckQuality(data)
data = bwa.Align(ref, data)
```

8. Click on **Run** button from the **Commands** panel below the code editor to execute the workflow.
9. **Job Histories** panel shows the executing/executed workflows. 
10. Click **Output** tab of **Results Panel** to view the output.

### Show prospective provenance (Section IV.D)
Prospective provenance shows the structure of a workflow. Click **Graph** button from the **Commands Panel** to show the prospective provenance of the workflow for a quick overview of the previous workflow.

### Show Retrospective provenance (Section IV.D)
Restrospective provenance shows the graph of an execution of a workflow. Follow these step to show a retrospective provenance query.
1. Hover mouse over and item on the **Job Histories** panel.
2. Click **Provenance** button on the floating toolbar of a history. Following code snippet in generated in the code editor. The *id* is the **run id** of workflow execution.

```
run = Run.Get(id = 6)
View.Graph(run)
```
3. Click on "Run" button below the code editor to show the retrospective provenance of a run of the workflow.

### Cross-domain Workflows
We present a cross-domain workflow below, which identifies biomarkers from both a FASTA file and a collection of image files by leveraging bioinformatics and image processing tools. The extracted biomarkers are then used to train a model, utilizing a machine learning classifier.

1. Click "+" button in code editor toolbar to create a new workflow.
2. Expand to /public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq and drag it to code editor. Rename the generated variable name *data* to *fasta*.
```
fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
```
3. Search *BioMarkers* on the **Services Panel** and drag the one under **Bioinformatics (bio)** group to the code editor. Replace input parameter *data* by *fasta*. Change the assigned variable from *data* to *fa_markers*.
```
fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
fa_markers = bio.BioMarkers(fasta)
```
4. Expand to /public/bioml/images and drag it to code editor. Rename the generated variable name *data* to *imgs*.
```
imgs = '/public/bioml/images'
```
5. Search *BioMarkers* on the **Services Panel** and drag the one under **Bioinformatics (img)** group to the code editor. Replace input parameter *data* by *imgs*. Change the assigned variable from *data* to *img_markers*.
```
imgs = '/public/bioml/images'
img_markers = img.BioMarkers(imgs)
```

6. The final workflow looks like below:

```
fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
fa_markers = bio.BioMarkers(fasta)

imgs = '/public/bioml/images'
img_markers = img.BioMarkers(imgs)
```

7. Click **Save** button on the **Code Editor** toolbar.
8. A window appears. Give a name for the workflow (e.g. *Biomarker Classifier Workflow*). Remember the generated **ID**.

**Now machine learning expert creates a classifier for Biomarkers.**

9. Now open another browser window and navigate to [http://localhost:8000](http://localhost:8000).
10. Log in using the username: **anonymous1@gmail.com** and password: **icse2025**.
11. Search **Workflows Panel** with the **ID** generated in Step 8. Once found, double click it. It will be loaded in the code editor.
12. Search *ClassifyBioMarker* on the **Services Panel** and drag the one under **Bioinformatics (ml)** group to the code editor. 
13. Replace input parameters *biodata* by *fa_markers* and *imgdata* by *img_markers*. If there is *model* parameter, remove it. 
14. Rename the generated *data* variable to *model*.

```
fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
fa_markers = bio.BioMarkers(fasta)

imgs = '/public/bioml/images'
img_markers = img.BioMarkers(imgs)

model = ml.ClassifyBioMarker(fa_markers, img_markers)
```
15. Click **Run** from the **Commands Panel** below the code editor to generate a classifier model from the the fasta file and images.

This workflow can be saved with parameters for fasta and imgs and return for model. Saved workflows can be called from another workflow using **Workflow** function. Details instructions can be found in the **Help Document**. For simpliciy, you will extend this workflow and use this classifier model to predict Biomarkers from a Fasta file and an image folder.

16. Expand to */public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq* and drag it to the code editor. Rename the generated variable name *data* to *fasta2*.
17. Expand to */public/bioml/images2* and drag it to code editor. Rename the generated variable name *data* to *imgs2*.
```
...
...
fasta2 = '/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq'
imgs2 = '/public/bioml/images2'
```

18. Search *PredictBioMarker* on the **Services Panel** and drag it to the code editor. Replace input parameter *biodata* by *fa_markers* and *imgdata* by *img_markers*.
```
fasta = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
fa_markers = bio.BioMarkers(fasta)

imgs = '/public/bioml/images'
img_markers = img.BioMarkers(imgs)

model = ml.ClassifyBioMarker(fa_markers, img_markers)

fasta2 = '/public/MiSeq_SOP/F3D149_S215_L001_R1_001.fastq'
imgs2 = '/public/bioml/images2'
fa_markers = bio.BioMarkers(fasta2)
img_markers = img.BioMarkers(imgs2)

data = ml.PredictBioMarker(fa_markers,img_markers,model)
```
19. Click **Run** from the **Commands Panel** below the code editor. This workflow first generates a classifier model from a fasta file and image folder. It then uses the model to predict Biomarkers of another fasta file and image folder.

### A workflow for NiCad clone detection

Here is an example workflow for NiCad clone detection (Listing I in the paper). The variables are initialized with default values. You can replace data with other source system.

```
data = '/public/swanalytics/luaj'
threshold = 0.30
granularity = 'blocks'
language = 'java'
transform = 'none'
rename = 'blind'
abstract = 'none'
cluster = 'yes'
report = 'yes'
include = ''
excluse = ''
miniclonesize = 10
maxclonesize = 2500
normalize = 'none'
filter = 'none'

nicad.CleanAll(dirname(data))

data = nicad.Extract(data,granularity=granularity,language=language)

# transform doesn't work for java
if transform != 'none':
    data = nicad.Transform(data,granularity=granularity,language=language,transform=transform)

data = nicad.Rename(data,granularity=granularity,language=language,renaming=rename)

if filter != 'none':
    data = nicad.Filter(data,granularity=granularity,language=language,nonterminals=filter)

if abstract != 'none':
    data = nicad.Abstract(data,granularity=granularity,language=language,nonterminals=abstract)

# normalize=none, so don't call it
if normalize != 'none':
    data = nicad.Normalize(data,granularity=granularity,language=language,normalizer=normalize)
data = nicad.FindClonePairs(data,threshold=threshold,minclonesize=minclonesize,maxclonesize=maxclonesize)
clones=data

if cluster == 'yes':
    data = nicad.ClusterPairs(data)

if report == 'yes':
    data = nicad.GetSource(data)
    data = nicad.MakePairHTML(data)
``` 

Click the **Run** button from the *Commands Panel** to execute the workflow. To test this workflow with other source systems, upload your source system using the **Dataset Panel** and change the *data* variable.

### Tool Integration
End-users can add an external tool to BioSocSys to extend its capabilities. Following types of tools can be integrated into the system:
- Python function
- Python module
- Python program
- Python program in venv (e.g., Python 2.7)
- Shell script (e.g., bash/sh)
- pip install
- pip install from requirements file
- New venv program
- Java program
- Tools from Docker container

### Workthrough of integrating a tool
Follow the steps below to create a custom tool using matplotlib and integrate it in BioSocSys. Since the executation model of BioSocSys is unattended execution (in contrast to interactive execution), __matplotlib.show__ will not work. The output must be saved as a file using __savefig__.

1. Click the **+** button in **Services** panel. **Add Service/Tool/Module** dialog will appear.
2. Select **Simple Adapter (Identity)** from the **Select Tool Type** dropdown.
3. Replace the code of the **Python Adapter** tab with the code below: 

```
from os import path
import matplotlib.pyplot as plt
def demo_service(context, *args, **kwargs):
	plt.plot(args[0], args[1])
	plt.xlabel('Months')
	plt.ylabel('Books Read')

	output = path.join(context.gettempdir(), 'books_read.png')
	plt.savefig(output)
	return output
```

4. Click **JSON Mapper** tab. 
5. Type *BookChartV3* in **name** text field.
6. Change **type** field of **Parameters** to __int[]__.
7. Click **+** below the **Parameters** title.
8. Change **name** to __data2__ and **type** to __int[]__.
9. Change **type** of **Returns** to __file__.
10. The JSON preview of the mapper is shown below:

```
{
    "package":"",
    "name":"BookChartV3",
    "params":[
        {
            "name":"data",
            "type":"int[]",
            "desc":""
        },
        {
            "name":"data2",
            "type":"int[]",
            "desc":""
        }
    ],
    "returns":[
        {
            "name":"data",
            "type":"file"
        }
    ]
}
```

11. Click **More...** from the **Function** section.
12. Add *matplotlib* in the **pippkgs** text box.
13. Click **Save** button.
14. Select **All** radio button in the **Services** panel.
15. Click **Reload** button in the **Services** panel.
16. *BookReadChart* tool appears in the **Services** list.

#### Testing new tool
To test the newly integrated tool, follow these steps:
1. Click **+** button in the **Code Editor** panel.
2. Select *BookReadChart* tool in the **Services** list and drag it to the **Code Editor**.
3. Replace *data* parameter with [1, 2, 3, 4, 5] and data2 with [100, 200, 150, 500, 400] in the generated code. The result code looks as below:

'''
data = demo.BookChartV3([1, 2, 3, 4, 5], [100, 200, 150, 500, 400])
'''
4. Click **Run** from the **Commands Panel** below the code editor. A .png file will be generated in the **Output** tab of the **Results Panel**.

The main reason behind this tool is to demonstrate that you can attach complex Python code and use any Python modules as tool while your workflow DSL script still remains abstracted from complex code.

Click **(i)** button in any panel to view the **Help** document. You will see instructions for integrating other types of tools.

# Conclusion
This document describes the instructions for the installation and evaluation of the SEIS-ICSE 2025 artifact for paper *A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0*. Further details about the framework can be found in the [GitHub repository](https://github.com/TechOptionsBD/vizsciflow/tree/vizsciflowdockfull) (vizsciflowdockfull branch).