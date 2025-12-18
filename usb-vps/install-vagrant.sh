#!/bin/bash

echo "📦 Installing Vagrant for USB VPS..."

# Install Vagrant via Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew first..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install vagrant
brew install virtualbox

echo "✅ Vagrant and VirtualBox installed!"
echo ""
echo "Next steps:"
echo "1. Insert your USB drive"
echo "2. Run: ./create-usb-vps.sh"