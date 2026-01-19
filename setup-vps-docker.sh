#!/bin/bash
# Script to set up Docker permissions on VPS
# Run this on your VPS

echo "=== Setting up Docker permissions ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
fi

# Add current user to docker group
echo "Adding user $(whoami) to docker group..."
sudo usermod -aG docker $USER

echo ""
echo "=== Docker setup complete ==="
echo ""
echo "IMPORTANT: You need to log out and log back in for the docker group"
echo "membership to take effect. Or run:"
echo "  newgrp docker"
echo ""
echo "To test Docker without sudo, run:"
echo "  docker ps"
echo ""
echo "If you see 'permission denied', log out and back in, or run 'newgrp docker'"

