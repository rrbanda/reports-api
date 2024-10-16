#!/bin/bash

# podman_setup.sh script

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
NETWORK_NAME="ai_network"
MONGODB_CONTAINER_NAME="mongodb"
FASTAPI_CONTAINER_NAME="fastapi_service"
MONGODB_PORT=27017
FASTAPI_PORT=8080  # Changed to 8080 as per user request
FASTAPI_IMAGE_NAME="fastapi_service"

# Create Podman network if it doesn't exist
if ! podman network exists $NETWORK_NAME; then
    echo "Creating Podman network: $NETWORK_NAME"
    podman network create $NETWORK_NAME
else
    echo "Podman network $NETWORK_NAME already exists."
fi

# Run MongoDB container with initialization scripts
if ! podman ps --format "{{.Names}}" | grep -qw $MONGODB_CONTAINER_NAME; then
    echo "Running MongoDB container: $MONGODB_CONTAINER_NAME"
    podman run -d \
        --name $MONGODB_CONTAINER_NAME \
        --network $NETWORK_NAME \
        -p $MONGODB_PORT:27017 \
        -e MONGO_INITDB_DATABASE=patient_db \
        -v "$(pwd)/app/init-mongo:/docker-entrypoint-initdb.d:ro" \
        mongo:latest
    echo "MongoDB container started."
else
    echo "MongoDB container $MONGODB_CONTAINER_NAME is already running."
fi

# Build FastAPI container image
echo "Building FastAPI container image: $FASTAPI_IMAGE_NAME"
podman build -t $FASTAPI_IMAGE_NAME .

# Run FastAPI container
if ! podman ps --format "{{.Names}}" | grep -qw $FASTAPI_CONTAINER_NAME; then
    echo "Running FastAPI container: $FASTAPI_CONTAINER_NAME"
    podman run -d \
        --name $FASTAPI_CONTAINER_NAME \
        --network $NETWORK_NAME \
        -p $FASTAPI_PORT:8000 \
        -e MONGODB_URI=mongodb://mongodb:27017 \
        $FASTAPI_IMAGE_NAME
    echo "FastAPI container started."
else
    echo "FastAPI container $FASTAPI_CONTAINER_NAME is already running."
fi

echo "All services are up and running."
