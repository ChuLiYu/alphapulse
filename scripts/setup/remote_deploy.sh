#!/bin/bash
# scripts/setup/remote_deploy.sh
# Robust automation script for AlphaPulse production deployment

set -e

echo "🚀 Starting AlphaPulse Production Deployment..."

# 1. Detect kubectl path
if [ -f "/usr/local/bin/kubectl" ]; then
    KUBECTL="/usr/local/bin/kubectl"
elif [ -f "/usr/bin/kubectl" ]; then
    KUBECTL="/usr/bin/kubectl"
else
    KUBECTL="kubectl" # Fallback to PATH
fi

# 2. Wait for K3s readiness
echo "⏳ Waiting for K3s to initialize..."
MAX_RETRIES=60
COUNT=0

while true; do
    if command -v "$KUBECTL" &> /dev/null && "$KUBECTL" get nodes | grep -q "Ready"; then
        echo "✅ K3s is Ready!"
        break
    fi
    
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo "❌ Timeout waiting for K3s."
        exit 1
    fi
    
    echo "Check count: $COUNT/$MAX_RETRIES... (K3s not ready yet)"
    sleep 5
    ((COUNT++))
done

# 3. Setup Namespace
"$KUBECTL" create namespace alphapulse 2>/dev/null || true

# 4. Setup Credentials
if ! command -v htpasswd &> /dev/null; then
    echo "📦 Installing httpd-tools..."
    dnf install httpd-tools -y
fi

echo "🔐 Configuring Admin Credentials..."
htpasswd -bc auth admin AlphaPulse2026
"$KUBECTL" create secret generic admin-credentials --from-file=auth -n alphapulse --dry-run=client -o yaml | "$KUBECTL" apply -f -
rm auth

# 5. Clone or Update Repository
DEPLOY_DIR="$HOME/deploy"
if [ -d "$DEPLOY_DIR/.git" ]; then
    echo "🔄 Updating repository..."
    cd "$DEPLOY_DIR"
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/ChuLiYu/alphapulse.git "$DEPLOY_DIR"
    cd "$DEPLOY_DIR"
fi

# 6. Apply Manifests
echo "🚢 Deploying services..."
"$KUBECTL" apply -k infra/k3s/base

echo "📊 Status:"
"$KUBECTL" get pods -n alphapulse
