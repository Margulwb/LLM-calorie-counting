#!/bin/bash

# Setup script for Rocky Linux 9
# LLM Weight Loss Expert Application

set -e

echo "=========================================="
echo "LLM Weight Loss Expert - Setup Script"
echo "Rocky Linux 9"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "1. Updating system packages..."
dnf update -y

# Install Python 3.9+
echo "2. Installing Python 3.9+..."
dnf install -y python3.9 python3.9-pip python3.9-devel

# Install required system packages
echo "3. Installing system dependencies..."
dnf install -y gcc gcc-c++ make git curl

# Install Ollama
echo "4. Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "Ollama already installed"
fi

# Start Ollama service
echo "5. Starting Ollama service..."
systemctl enable ollama
systemctl start ollama

# Pull Mistral model
echo "6. Pulling Mistral 7B model (this may take a while)..."
ollama pull mistral

# Create application user
echo "7. Creating application user..."
if ! id "llmapp" &>/dev/null; then
    useradd -r -s /bin/bash -d /opt/llm-calorie-app llmapp
fi

# Create application directory
echo "8. Setting up application directory..."
APP_DIR="/opt/llm-calorie-app"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone or copy application files
if [ -d "/tmp/llm-calorie-counting" ]; then
    echo "Copying application files..."
    cp -r /tmp/llm-calorie-counting/* $APP_DIR/
else
    echo "Application files should be in $APP_DIR"
fi

# Create virtual environment
echo "9. Creating Python virtual environment..."
python3.9 -m venv $APP_DIR/venv

# Activate virtual environment and install dependencies
echo "10. Installing Python dependencies..."
source $APP_DIR/venv/bin/activate
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

# Create .env file
echo "11. Creating environment configuration..."
if [ ! -f "$APP_DIR/.env" ]; then
    cp $APP_DIR/.env.example $APP_DIR/.env
    echo "Created .env file - please review and update if needed"
fi

# Set permissions
echo "12. Setting permissions..."
chown -R llmapp:llmapp $APP_DIR
chmod +x $APP_DIR/backend/app.py

# Install systemd service
echo "13. Installing systemd service..."
cp $APP_DIR/configs/llm-calorie-app.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable llm-calorie-app

# Configure firewall
echo "14. Configuring firewall..."
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=5000/tcp
    firewall-cmd --reload
fi

# Initialize vector database
echo "15. Initializing knowledge base..."
cd $APP_DIR
source venv/bin/activate
python3 -c "from backend.services.llm_service import LLMService; LLMService()" || echo "Knowledge base will be initialized on first run"

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  sudo systemctl start llm-calorie-app"
echo ""
echo "To check status:"
echo "  sudo systemctl status llm-calorie-app"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u llm-calorie-app -f"
echo ""
echo "API will be available at: http://localhost:5000"
echo ""
echo "Test the API:"
echo "  curl http://localhost:5000/health"
echo ""
