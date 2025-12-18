#!/bin/bash

echo "☁️ Creating DigitalOcean VPS..."

# Install doctl (DigitalOcean CLI)
if ! command -v doctl &> /dev/null; then
    echo "Installing DigitalOcean CLI..."
    brew install doctl
fi

# Generate SSH key if it doesn't exist
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
fi

echo ""
echo "🔑 Setup Instructions:"
echo "1. Create account at https://cloud.digitalocean.com"
echo "2. Generate API token in API section"
echo "3. Run: doctl auth init"
echo "4. Add SSH key: doctl compute ssh-key import my-key --public-key-file ~/.ssh/id_rsa.pub"
echo "5. Create VPS: doctl compute droplet create my-vps --region nyc1 --image ubuntu-22-04-x64 --size s-1vcpu-1gb --ssh-keys \$(doctl compute ssh-key list --format ID --no-header)"
echo ""
echo "💰 Cost: ~\$6/month for basic VPS"