#!/bin/bash

# --- CONFIG ---
# Replace this with your container name or ID
CONTAINER_NAME="kingfisher-app:latest"

# --- FUNCTION ---
echo "Stopping container: $CONTAINER_NAME..."
docker stop "$CONTAINER_NAME" 2>/dev/null

echo "Removing container: $CONTAINER_NAME..."
docker rm "$CONTAINER_NAME" 2>/dev/null

# Optional: remove dangling volumes
echo "Cleaning up dangling volumes..."
docker volume prune -f

# Optional: remove dangling images
echo "Cleaning up dangling images..."
docker image prune -f

# Optional: remove unused networks
echo "Cleaning up unused networks..."
docker network prune -f

echo "Docker cleanup completed."
