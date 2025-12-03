#!/bin/bash
set -e

echo "Setting up MSIFanControl..."

# 1. Install System Dependencies
echo "Installing system dependencies..."
if command -v dnf >/dev/null 2>&1; then
    sudo dnf check-update || true
    sudo dnf install -y python3-virtualenv gobject-introspection-devel cairo-gobject-devel cairo-devel python3-devel gtk4-devel libadwaita-devel
elif command -v apt >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y python3-virtualenv python3-venv libgirepository1.0-dev libcairo2-dev libgtk-4-dev libadwaita-1-dev
else
    echo "Unsupported package manager. Please install dependencies manually."
fi

# 2. Create Virtual Environment
echo "Creating virtual environment in .venv..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# 3. Install Python Dependencies
echo "Installing Python dependencies..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install PyGObject pycairo

# 4. Setup EC Module
echo "Setting up EC module..."
# Check if we need to build it
if ! modprobe -n ec_sys >/dev/null 2>&1; then
    echo "ec_sys module not found. Running fix script..."
    # We need to move the fix script back or reference it from legacy if we want to reuse it.
    # But I should probably put a clean version in scripts/
    if [ -f "legacy/fix_ec_sys.sh" ]; then
        cp legacy/fix_ec_sys.sh scripts/fix_ec_sys.sh
        chmod +x scripts/fix_ec_sys.sh
        ./scripts/fix_ec_sys.sh
    else
        echo "Error: fix_ec_sys.sh not found."
    fi
fi

# Ensure module loading on boot
echo "Configuring module loading..."
echo "options ec_sys write_support=1" | sudo tee /etc/modprobe.d/ec_sys.conf > /dev/null
echo "ec_sys" | sudo tee /etc/modules-load.d/ec_sys.conf > /dev/null

# Load it now
sudo modprobe ec_sys write_support=1 || true

echo "Setup complete! Run 'task run' to start."
