#!/bin/bash

# Setup script for CDK v2 environment
# This script ensures a clean CDK v2 setup without v1 conflicts

echo "🔧 Setting up CDK v2 environment..."

# Remove existing virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf .venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install all dependencies from main requirements.txt
echo "Installing all dependencies..."
cd ..
pip install -r requirements.txt
cd infra

# Verify installation
echo "Verifying CDK v2 installation..."
export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true
python -c "from aws_cdk import Stack; print('CDK v2 setup successful!')"

# Acknowledge CDK notice to clean up future outputs
echo "Configuring CDK environment..."
cdk acknowledge 34892 > /dev/null 2>&1

echo ""
echo "    Setup complete! You can now:"
echo "  - Activate the environment: source .venv/bin/activate"
echo "  - Deploy the stack: cdk deploy"
echo "  - If you see Node.js warnings, silence them with:"
echo "    export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true" 