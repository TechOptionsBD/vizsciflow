# A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0 (Artifact)
This document contains the instructions for the SEIS-ICSE 2025 artifact evaluation for paper *A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0*. This paper proposes a novel framework for the cross-domain computational scientific experiment in the context of Society 5.0 and develops a proof-of-concept prototype of a scientific workflow management system (SWfMS) based on the proposed framework. Researchers from different scientific domains can use this multi-user, web-based system to design and execute interdisciplinary workflows collaboratively. The artifact provides instructions to reproduce the experiments (Section VII) reported in the paper. This document is also available online at [BioSocSys GitHub Repository](https://github.com/TechOptionsBD/BioSocSys/blob/BioSocSysdockfull/README.md).

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

To address these challenges, we developed a prototype scientific workflow management system (SWfMS) for code clone analysis, bioinformatics, image processing, and machine learning by integrating tools and services from their respective domains. This README provides instructions for the ICSE 2025 Artifact Evaluation Track, associated with the paper A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0, accepted in the ICSE 2025 SEIS Track. It includes steps to obtain, install, recreate, and exercise the developed SWfMS.

## Preparing the artifact
The artifact is prepared as a pre-built Docker image, which includes all necessary dependencies and third-party tools. Users can run this Docker image on Ubuntu 20.04+ (also compatible with Windows 11 WSL). To get started, download [vizsciflowfull.tar](https://dx.doi.org/10.6084/m9.figshare.28224869) (DOI: 10.6084/m9.figshare.28224869) and run the following command to load the image from the .tar file (note that you may need *root privileges* to run docker):

```
$ docker load -i vizsciflowfull.tar
```

## Making the artifact available
The artifact is made available through Figshare, a long-term data archival repository. A DOI, 10.6084/m9.figshare.28224869, has been generated for it. The artifact can be downloaded from [Figshare link](https://dx.doi.org/10.6084/m9.figshare.28224869).

## Documenting the artifact
We have compiled all documentation in this README.md file. A separate LICENSE file is also submitted with the uploaded package. This document details the purpose, proveance, data, setup, and usage of the artifact. 

## Purpose
The artifact is a proof-of-concept implementation of a scientific workflow management system (SWfMS) designed for cross-domain collaborative scientific experiments. It features an intuitive web interface that allows researchers to design scientific workflows using a domain-specific language (DSL). Visual support tools and secondary notation facilitate quick workflow code generation. Users can drag and drop workflow artifacts — such as datasets, tools, templates, and histories — presented as graphical elements into the code editor, which then generates the corresponding code snippets. Additionally, a control flow graph provides a quick overview of the workflow.

### Badges Applying For

1. **Available** (Artifact is placed on a publicly accessible archival repository): The artifact is permanently available through Figshare, and a DOI has been created for it. Please check [**Making the artifact available**](#making-the-artifact-available) for details.
2. **Functional** (Artifact is documented, consistent, complete, exercisable, and includes appropriate evidence of verification and validation): This README file provides detailed instructions for installation and describes how to accomplish the exercises outlined in the associated paper. Additionally, once installed, the artifact offers a comprehensive help document detailing installation, language feature, workflow design, tool integration, and so on.
3. **Reusable** (Artifact significantly exceeds minimal functionality): The artifact is well-documented and includes a step-by-step guide for designing workflows and integrating different types of tools. A number of sample workflows are also provided to help users get started. Several scripts are included to create this artifact. The datasets necessary to run the workflows shown in the paper are included in the Docker image. Users can also quickly upload new dataset using the *upload feature* of the **Dataset Panel**.

## Provenance

The artifact is available as a pre-built Docker image, which has all dependencies and third-party tools installed. Download [vizsciflowfull.tar](https://dx.doi.org/10.6084/m9.figshare.28224869) (DOI: 10.6084/m9.figshare.28224869) and run the following command on it to obtain the Docker image (you may need root privilege to run `docker`):

```
$ docker load -i vizsciflowfull.tar
```

### Start the Docker Container

To instantiate the Docker image, run the following command.

```
$ docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull:latest
```

A Docker container named *vizsciflowfull* will be instantiated. Now browse to [http://localhost:8000](http://localhost:8000) to access the BioSocSys web interface. Use username 'testuser@gmail.com' and password 'test2025' to login. 

Once running inside the Docker, you can also find this document at `/home/vizsciflow/README.md`.

### Build the Docker Image

The script used to build the Docker image can be found at `/home/vizsciflow/setupsingledocker.sh` inside the running. It can also be found in [BioSocSys's Github repository](https://github.com/TechOptionsBD/BioSocSys/blob/BioSocSysdockfull/README.md). Using this script, one can rebuild the Docker image from scratch or install our artifact on a clean Ubuntu 20.04+ machine (compatible also with ).

The steps for building the Docker image are outlined in the script below. Read the *echo* commands for details of the steps. It is **not** necessary for the artifact evaluation to rebuild the image, but would be useful for anyone who would like to reuse or deploy BioSocSys.

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

echo "Download templates/workflows and copy in ./workflows file"
if [ -f ./workflows ]; then
    sudo rm -f ./workflows
fi
echo "Downloading workflows from https://docs.google.com/document/d/1Kg5yCnhVb0QNIyqDmjNQWXICqPzUdoXL4PgtCz7F6BU/edit?usp=sharing"
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Kg5yCnhVb0QNIyqDmjNQWXICqPzUdoXL4PgtCz7F6BU' -O workflows

echo "Build docker image"
docker build --build-arg UID=`id -u` -t vizsciflowfull:latest .
echo "Run the docker image as vizsciflowfull container"
docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull:latest

echo "Waiting for PostgreSQL to finish start."
docker exec vizsciflowfull sh -c "/home/vizsciflow/wait_for_pg_ready.sh"

echo "Inserting the default values in the database ..."
docker exec vizsciflowfull sh -c "PGPASSWORD='sr-hadoop' psql -U phenodoop -d biowl -f /home/vizsciflow/vizsciflow.sql"

echo "Adding modules from ./src/plugins/modules to the database"
docker exec -i vizsciflowfull sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertmodules --path /home/vizsciflow/src/plugins/modules --with-users False --install-pypi False)'

echo "Adding workflows from ./workflows to the database"
docker exec -i vizsciflowfull sh -c '(cd /home/vizsciflow/src && /home/venvs/.venv/bin/flask --app manage insertworkflows --path /home/vizsciflow/workflows)'

echo "Commiting the changes of vizsciflowfull container into vizsciflowfull image."
docker commit vizsciflowfull vizsciflowfull:latest
echo "Saving the image in .tar file"
docker save vizsciflowfull:latest > vizsciflowfull.tar
```

## Setup
### Hardware Requirements
The artifact supports x86-64 architecture running Linux-based operating systems. It has been tested with 12 CPU cores and 32GB of memory. 

### Software Dependencies

The Docker image runs Debian GNU/Linux 11 (bullseye) built from python:3.10-bullseye DockerHub image Ubuntu 24.04. It implements a cross-domain SWfMS and integrates tools from bioinformatics, machine learning, image processing tools.


The Docker image contains the following software dependencies:
- Python 10.0
- PostgreSQL 13.4
- Flask 2.0.1
- Java Virtual Machine 11.0.11

Tools integrated in the SWfMS:
- FastQC
- BWA-MEM
- PEAR

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

**Expected Time: 15 minutes**

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
7. Return the output data.
```
return data
```
8. Steps 3-7 creates the following lines in the code editor.

```
data = '/public/MiSeq_SOP/F3D3_S191_L001_R1_001.fastq'
ref = '/public/genomes/Chr1.cdna'
html,zip = fastqc.CheckQuality(data)
data = bwa.Align(ref, data)
return data
```
9. Click on **Run** button from the **Commands** panel below the code editor to execute the workflow.
10. **Job Histories** panel shows the executing/executed workflows. 
11. Click **Output** tab of **Results Panel** to view the output.

### Show prospective provenance
Prospective provenance shows the structure of a workflow. Click **Graph** button from the **Commands Panel** to show the prospective provenance of the workflow for a quick overview of the previous workflow.

### Show Retrospective provenance
Restrospective provenance shows the graph of  
1. Hover mouse over and item on the **Job Histories** panel.
2. Click **Provenance** button on the floating toolbar of a history. Following code snippet in generated in the code editor. The _id_ will the **run id** of workflow execution.

```
run = Run.Get(id = 6)
View.Graph(run)
```

3. Click on "Graph" button below the code editor to show the retrospective provenance of a run of the workflow.

### Cross-domain Workflows
We present a cross-domain workflow below, which identifies biomarkers from both a FASTA file and an image file by leveraging bioinformatics and image processing Docker containers. The extracted biomarkers are then used to train a model, utilizing a machine learning Docker container classifier.

```  
# parameters: fasta, image
# returns: model

parallel:
    # Bio-markers from bioinformatics docker
    fa_markers = bio.BioMarkers(fasta)
with:
    # Bio-markers from image processing docker
    img_markers = img.BioMarkers(image)

# Train model from machine learning docker, 
# save it to a file and return the file name.
return bioml.BioClassify(fa_markers, img_markers)
```

We have here another cross-domain workflow, where bioinformatics and image processing tools are integrated to predict biomarkers using a machine learning model.

```
# parameters: fasta, image, model
# returns: prediction

parallel:
    # Bio-markers from bioinformatics docker
    fa_markers = bio.BioMarkers(fasta)
with:
    # Bio-markers from image processing docker
    img_markers = img.BioMarkers(image)

# Predict from machine learning docker
return bioml.BioPredict(model, fa_markers, img_markers)
```

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
2. Select **Simple Adapter (Identity)** from the **Select Tool Type** dropdown menu.
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
5. Type __BookChartV3__ in **name** text field.
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

11. Add __matplotlib__ in the **pip install** text box.
12. Click **Add** button. 
13. Select **All** radio button and then click **Reload** button in the **Services** panel.
14. __BookReadChart__ tool appears in the **Services** list.

#### Testing new tool
To test the newly integrated tool, follow these steps:
1. Click **+** button in the **Code Editor** panel.
2. Select __BookReadChart__ tool in the **Services** list and drag it to the **Code Editor**.
3. Change __data__ parameter to __50__ and __data2__ to __200__ in the generated code.
4. The result code looks as below:

'''
data = BookReadChart(50, 200)
'''

The main reason behind this tool is to demonstrate that you can attach complex Python code and use any Python modules as tool while your workflow DSL script still remains abstracted from complex code.

Click **(i)** button in any panel to view the **Help** document. You will see instructions for integrating other types of tools.

# Conclusion
This document describes the instructions for the installation and evaluation of the SEIS-ICSE 2025 artifact for paper *A Collaborative Framework for Cross-Domain Scientific Experiments for Society 5.0*. Further details about the framework can be found in the [GitHub repository](https://github.com/TechOptionsBD/vizsciflow/tree/vizsciflowdockfull).