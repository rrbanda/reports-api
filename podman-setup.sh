#!/bin/bash

# podman_setup.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
NETWORK_NAME="ai_network"
NEO4J_CONTAINER_NAME="neo4j"
FASTAPI_CONTAINER_NAME="fastapi_service"
NEO4J_PORT_HTTP=7474
NEO4J_PORT_BOLT=7687
FASTAPI_PORT=8080
FASTAPI_IMAGE_NAME="fastapi_service"

# Create Podman network if it doesn't exist
if ! podman network exists $NETWORK_NAME; then
    echo "Creating Podman network: $NETWORK_NAME"
    podman network create $NETWORK_NAME
else
    echo "Podman network $NETWORK_NAME already exists."
fi

# Run Neo4j container
if ! podman ps --format "{{.Names}}" | grep -qw $NEO4J_CONTAINER_NAME; then
    echo "Running Neo4j container: $NEO4J_CONTAINER_NAME"
    podman run -d \
        --name $NEO4J_CONTAINER_NAME \
        --network $NETWORK_NAME \
        -p $NEO4J_PORT_HTTP:7474 \
        -p $NEO4J_PORT_BOLT:7687 \
        -e NEO4J_AUTH=neo4j/password \
        neo4j:latest
    echo "Neo4j container started."
else
    echo "Neo4j container $NEO4J_CONTAINER_NAME is already running."
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
        --env-file app/.env \
        $FASTAPI_IMAGE_NAME
    echo "FastAPI container started."
else
    echo "FastAPI container $FASTAPI_CONTAINER_NAME is already running."
fi

echo "All services are up and running."
