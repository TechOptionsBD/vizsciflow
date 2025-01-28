#!/bin/bash

# Check if the tar file path is provided as an argument
# if [ -z "$1" ]; then
#     echo "Usage: $0 path/to/your/image.tar"
#     exit 1
# fi

# Default tar file path
DEFAULT_TAR_FILE_PATH="vizsciflowfull.tar"

# Use the provided argument as the tar file path, or default if not provided
TAR_FILE_PATH="${1:-$DEFAULT_TAR_FILE_PATH}"

# Check if the container 'vizsciflowfull' already exists
echo "Delete existing vizsciflowfull containers ..."
if [ $(docker ps -a -q -f name=vizsciflowfull) ]; then
    # Stop the container if it is running
    docker stop vizsciflowfull
    # Remove the container
    docker rm vizsciflowfull
fi

# Load the Docker image from the tar file
echo "Loading the image from the $TAR_FILE_PATH file ..."
docker load -i $TAR_FILE_PATH

# Get the image ID of the loaded image
# IMAGE_ID=$(docker images -q | head -n 1)

# Run a container from the loaded image with the specified name and execute the run.sh script
echo "Starting vizsciflowfull container ..."
docker run -d -p 8000:8000 --name vizsciflowfull vizsciflowfull /bin/bash -c "cd ~/src && ./run.sh"

echo "Container vizsciflowfull started."
