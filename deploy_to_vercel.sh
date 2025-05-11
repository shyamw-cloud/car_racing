#!/bin/bash

echo "===== Car Racing Game Vercel Deployment ====="
echo

echo "Step 1: Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed or not in PATH."
    echo "Please install Node.js from https://nodejs.org/"
    echo "and run this script again."
    exit 1
fi
echo "Node.js found!"

echo
echo "Step 2: Installing Vercel CLI..."
npm install -g vercel
if [ $? -ne 0 ]; then
    echo "Failed to install Vercel CLI."
    exit 1
fi

echo
echo "Step 3: Building the game..."
python3 simple_deploy.py
if [ $? -ne 0 ]; then
    echo "Failed to build the game."
    exit 1
fi

echo
echo "Step 4: Deploying to Vercel..."
cd build/web
vercel
if [ $? -ne 0 ]; then
    echo "Deployment failed."
    exit 1
fi

echo
echo "Deployment completed successfully!"
echo "Your game should now be available at the URL provided by Vercel."