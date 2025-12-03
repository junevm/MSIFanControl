#!/bin/bash
set -e

echo "Detected missing ec_sys module. This script will rebuild the ACPI drivers from Fedora kernel source with EC debugfs enabled."
echo "This process may take some time and requires downloading kernel sources (~150MB)."

# Install necessary tools
echo "Installing build tools..."
sudo dnf install -y dnf-utils rpmdevtools ncurses-devel pesign elfutils-libelf-devel openssl-devel bison flex kernel-devel-$(uname -r)

# Setup RPM build tree
echo "Setting up RPM build tree..."
rpmdev-setuptree

# Create a temp dir for downloading source
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"

# Enable source repos and download kernel source
echo "Downloading kernel source..."
# We try to enable source repos just in case
sudo dnf config-manager --set-enabled fedora-source updates-source || true
dnf download --source kernel-$(uname -r)

SRC_RPM=$(ls kernel-*.src.rpm)
if [ -z "$SRC_RPM" ]; then
    echo "Failed to download kernel source RPM."
    exit 1
fi

# Install build dependencies for the kernel
echo "Installing kernel build dependencies..."
sudo dnf builddep -y "$SRC_RPM"

# Install the source RPM
echo "Installing source RPM..."
rpm -Uvh "$SRC_RPM"

# Prepare the kernel source tree
echo "Preparing kernel source tree..."
cd ~/rpmbuild/SPECS
rpmbuild -bp --target=$(uname -m) kernel.spec

# Find the build directory
BUILD_DIR=~/rpmbuild/BUILD/kernel-$(uname -r | cut -d- -f1)-build/kernel-$(uname -r | cut -d- -f1)/linux-$(uname -r)
# The path might vary slightly depending on Fedora version, let's try to find it dynamically if the above fails
if [ ! -d "$BUILD_DIR" ]; then
    BUILD_DIR=$(find ~/rpmbuild/BUILD -maxdepth 3 -name "linux-*" -type d | head -n 1)
fi

if [ ! -d "$BUILD_DIR" ]; then
    echo "Could not find kernel build directory."
    exit 1
fi

cd "$BUILD_DIR"

echo "Patching Makefile to match running kernel version..."
# Extract the extra version part (everything after the numeric version X.Y.Z)
# e.g. for 6.17.9-300.fc43.x86_64, we want -300.fc43.x86_64
EXTRAVERSION=$(uname -r | sed -E 's/^[0-9]+\.[0-9]+\.[0-9]+//')
sed -i "s/^EXTRAVERSION =.*/EXTRAVERSION = $EXTRAVERSION/" Makefile

echo "Configuring kernel..."
# Copy current config
cp /boot/config-$(uname -r) .config

# Enable ACPI_EC_DEBUGFS
# We use scripts/config if available, or just append/sed
if [ -f scripts/config ]; then
    ./scripts/config --module CONFIG_ACPI_EC_DEBUGFS
else
    echo "CONFIG_ACPI_EC_DEBUGFS=m" >> .config
fi

# Prepare for module build
echo "Preparing build..."
make modules_prepare

# Copy Module.symvers from kernel-devel to avoid missing symbol errors
if [ -f /usr/src/kernels/$(uname -r)/Module.symvers ]; then
    echo "Copying Module.symvers from /usr/src/kernels/$(uname -r)/..."
    cp /usr/src/kernels/$(uname -r)/Module.symvers .
fi

# Build ACPI drivers
echo "Building ACPI modules..."
# Allow unresolved symbols (common when building partial tree)
export KBUILD_MODPOST_WARN=1
make M=drivers/acpi modules

# Install the module
echo "Installing ec_sys module..."
# We only want to install ec_sys.ko, but make modules_install might install all acpi modules.
# Let's try to be specific or just copy it.
if [ -f drivers/acpi/ec_sys.ko ]; then
    sudo mkdir -p /lib/modules/$(uname -r)/extra
    sudo cp drivers/acpi/ec_sys.ko /lib/modules/$(uname -r)/extra/ec_sys.ko
    sudo depmod -a
else
    echo "ec_sys.ko not found after build."
    exit 1
fi

echo "Loading module..."
if sudo modprobe ec_sys write_support=1; then
    echo "Success! ec_sys module installed and loaded."
else
    echo "Failed to load module."
    echo "dmesg output:"
    sudo dmesg | tail -n 20
    exit 1
fi
