#!/bin/bash
# Script to fix SSH permissions on VPS
# Run this on your VPS as the user (github), not as root

echo "=== Fixing SSH Permissions ==="
echo "Current user: $(whoami)"
echo ""

# Fix home directory permissions
echo "1. Fixing home directory permissions..."
chmod 755 ~
echo "   Home directory: $(ls -ld ~ | awk '{print $1, $3, $4}')"

# Create .ssh directory if it doesn't exist
echo ""
echo "2. Creating/fixing .ssh directory..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "   .ssh directory: $(ls -ld ~/.ssh | awk '{print $1, $3, $4}')"

# Fix authorized_keys permissions
echo ""
echo "3. Fixing authorized_keys permissions..."
if [ -f ~/.ssh/authorized_keys ]; then
    chmod 600 ~/.ssh/authorized_keys
    echo "   authorized_keys: $(ls -l ~/.ssh/authorized_keys | awk '{print $1, $3, $4}')"
    echo "   Number of keys: $(wc -l < ~/.ssh/authorized_keys)"
else
    echo "   WARNING: ~/.ssh/authorized_keys does not exist!"
    echo "   You need to add your public key to this file."
fi

# Fix ownership
echo ""
echo "4. Fixing ownership..."
chown -R $USER:$USER ~/.ssh
echo "   Ownership fixed"

# Verify permissions
echo ""
echo "=== Verification ==="
echo "Home directory:"
ls -ld ~
echo ""
echo ".ssh directory:"
ls -ld ~/.ssh
echo ""
if [ -f ~/.ssh/authorized_keys ]; then
    echo "authorized_keys:"
    ls -l ~/.ssh/authorized_keys
    echo ""
    echo "First few lines of authorized_keys:"
    head -2 ~/.ssh/authorized_keys
else
    echo "authorized_keys: FILE DOES NOT EXIST"
    echo ""
    echo "To add your public key, run:"
    echo "  echo 'YOUR_PUBLIC_KEY' >> ~/.ssh/authorized_keys"
    echo "  chmod 600 ~/.ssh/authorized_keys"
fi

echo ""
echo "=== Done ==="
echo "If authorized_keys exists and has correct permissions, SSH should work."
echo "Test from your local machine:"
echo "  ssh -i github_actions_vm github@4.145.116.160"

