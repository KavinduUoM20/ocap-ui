#!/bin/bash

# Deployment script for VPS
# This script can be run manually on the VPS or used as a reference

set -e

IMAGE_NAME="${DOCKER_USERNAME:-your-username}/ocap-ui:latest"
CONTAINER_NAME="ocap-ui"
APP_DIR="/opt/ocap-ui"
PORT=8501

echo "Starting deployment of $IMAGE_NAME..."

# Login to Docker Hub (if needed for private images)
# echo $DOCKER_TOKEN | docker login -u $DOCKER_USERNAME --password-stdin

# Pull the latest image
echo "Pulling latest image..."
docker pull $IMAGE_NAME

# Stop and remove old container
echo "Stopping old container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Ensure .env file exists
mkdir -p $APP_DIR
if [ ! -f $APP_DIR/.env ]; then
    echo "ERROR: .env file not found at $APP_DIR/.env"
    echo "Please create it with BASE_URL configuration:"
    echo "  echo 'BASE_URL=http://your-api-url:8000/api/v1' > $APP_DIR/.env"
    exit 1
fi

# Run new container
echo "Starting new container..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p $PORT:8501 \
    --env-file $APP_DIR/.env \
    $IMAGE_NAME

# Clean up unused images
echo "Cleaning up unused images..."
docker image prune -f

echo "Deployment complete!"
echo "Container is running on port $PORT"
docker ps | grep $CONTAINER_NAME

