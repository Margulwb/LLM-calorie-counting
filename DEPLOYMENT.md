# 🚀 Deployment Guide - LLM Weight Loss Expert

## Quick Start Deployment

### Option 1: Rocky Linux 9 (Automated)

**Recommended for production servers**

1. **Prepare server:**
```bash
# Update system
sudo dnf update -y

# Install git
sudo dnf install git -y
```

2. **Clone and deploy:**
```bash
# Clone repository
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting

# Run automated setup (requires root)
sudo bash setup_rocky9.sh
```

3. **Verify deployment:**
```bash
# Check service status
sudo systemctl status llm-calorie-app
sudo systemctl status ollama

# Test API
curl http://localhost:5000/health

# View logs
sudo journalctl -u llm-calorie-app -f
```

**That's it!** Your application is now running as a systemd service.

---

### Option 2: Docker Deployment

**Recommended for containerized environments**

1. **Prerequisites:**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **Deploy:**
```bash
# Clone repository
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting/docker

# Start services
docker-compose up -d

# Wait for Ollama to download model (first time only)
docker-compose logs -f ollama
# Press Ctrl+C when you see "success"

# Verify
docker-compose ps
curl http://localhost:5000/health
```

3. **Access:**
- API: `http://your-server:5000`
- Frontend: `http://your-server:8080`

---

### Option 3: Manual Deployment

**For custom setups or development**

1. **System dependencies:**
```bash
# Rocky Linux / RHEL / CentOS
sudo dnf install python3.9 python3.9-pip python3.9-devel gcc g++ make git curl -y

# Ubuntu / Debian
sudo apt-get update
sudo apt-get install python3.9 python3.9-pip python3.9-venv gcc g++ make git curl -y
```

2. **Install Ollama:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
sudo systemctl start ollama
sudo systemctl enable ollama
ollama pull mistral
```

3. **Setup application:**
```bash
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env if needed

# Run
python backend/app.py
```

---

## Production Configuration

### 1. Reverse Proxy (Nginx)

**Install Nginx:**
```bash
sudo dnf install nginx -y  # Rocky/RHEL
# or
sudo apt-get install nginx -y  # Ubuntu
```

**Configure SSL with Let's Encrypt:**
```bash
# Install certbot
sudo dnf install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com
```

**Nginx configuration:**
```nginx
# /etc/nginx/conf.d/llm-calorie-app.conf

upstream llm_backend {
    server localhost:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        root /opt/llm-calorie-app/frontend;
        try_files $uri $uri/ /index.html;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://llm_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts for LLM responses
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /health {
        proxy_pass http://llm_backend;
    }
}
```

**Enable and start Nginx:**
```bash
sudo systemctl enable nginx
sudo systemctl start nginx

# Test configuration
sudo nginx -t

# Reload if OK
sudo systemctl reload nginx
```

### 2. Firewall Configuration

**Rocky Linux / RHEL (firewalld):**
```bash
# Allow HTTP and HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# If accessing API directly (not through Nginx)
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

**Ubuntu (ufw):**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 3. Performance Optimization

**For better LLM performance:**

1. **Use GPU (if available):**
```bash
# Install NVIDIA drivers and CUDA
# Then Ollama will automatically use GPU

# Verify GPU usage
nvidia-smi
```

2. **Optimize model:**
```bash
# Use quantized model for faster inference
ollama pull mistral:7b-instruct-q4_0

# Update .env
OLLAMA_MODEL=mistral:7b-instruct-q4_0
```

3. **Increase system resources:**
```bash
# Edit systemd service
sudo systemctl edit llm-calorie-app

# Add:
[Service]
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

### 4. Monitoring

**Setup monitoring with journald:**
```bash
# View logs
sudo journalctl -u llm-calorie-app -f

# Export logs
sudo journalctl -u llm-calorie-app --since today > app.log
```

**Setup log rotation:**
```bash
# Create /etc/logrotate.d/llm-calorie-app
sudo tee /etc/logrotate.d/llm-calorie-app <<EOF
/var/log/llm-calorie-app/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 llmapp llmapp
    sharedscripts
    postrotate
        systemctl reload llm-calorie-app > /dev/null 2>&1 || true
    endscript
}
EOF
```

### 5. Backup

**Backup vector database:**
```bash
# Create backup directory
sudo mkdir -p /backup/llm-calorie-app

# Backup script
sudo tee /usr/local/bin/backup-llm-app.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/backup/llm-calorie-app"
APP_DIR="/opt/llm-calorie-app"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup chroma_db
tar -czf "$BACKUP_DIR/chroma_db_$DATE.tar.gz" -C "$APP_DIR" chroma_db

# Keep only last 7 days
find "$BACKUP_DIR" -name "chroma_db_*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup-llm-app.sh

# Add to cron
echo "0 2 * * * /usr/local/bin/backup-llm-app.sh" | sudo crontab -
```

---

## Scaling

### Horizontal Scaling (Multiple Instances)

1. **Deploy multiple backends:**
```bash
# Instance 1 on port 5000
# Instance 2 on port 5001
# Instance 3 on port 5002
```

2. **Nginx load balancing:**
```nginx
upstream llm_backend {
    least_conn;
    server localhost:5000;
    server localhost:5001;
    server localhost:5002;
}
```

### Vertical Scaling

1. **Increase resources:**
   - More RAM for model caching
   - Better CPU/GPU for faster inference
   - SSD for faster vector DB access

2. **Optimize Ollama:**
```bash
# Edit /etc/systemd/system/ollama.service
[Service]
Environment="OLLAMA_MAX_LOADED_MODELS=2"
Environment="OLLAMA_NUM_PARALLEL=4"
```

---

## Health Checks

**Automated health monitoring:**
```bash
# Create health check script
sudo tee /usr/local/bin/health-check-llm.sh <<'EOF'
#!/bin/bash

# Check API
if ! curl -sf http://localhost:5000/health > /dev/null; then
    echo "API is down, restarting..."
    systemctl restart llm-calorie-app
    
    # Send alert (configure your notification method)
    # mail -s "LLM App Down" admin@example.com < /dev/null
fi

# Check Ollama
if ! curl -sf http://localhost:11434/api/version > /dev/null; then
    echo "Ollama is down, restarting..."
    systemctl restart ollama
fi
EOF

sudo chmod +x /usr/local/bin/health-check-llm.sh

# Run every 5 minutes
echo "*/5 * * * * /usr/local/bin/health-check-llm.sh" | sudo crontab -
```

---

## Troubleshooting

### Common Issues

1. **Port already in use:**
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process or change port in .env
```

2. **Ollama connection refused:**
```bash
# Check Ollama status
sudo systemctl status ollama

# Restart Ollama
sudo systemctl restart ollama

# Check if model is downloaded
ollama list
```

3. **Out of memory:**
```bash
# Use smaller model
ollama pull mistral:7b-instruct-q4_0

# Or increase swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

4. **Slow responses:**
```bash
# Check CPU/RAM usage
top
htop

# Check GPU usage (if available)
nvidia-smi

# Restart services
sudo systemctl restart ollama
sudo systemctl restart llm-calorie-app
```

---

## Updates

**Update application:**
```bash
cd /opt/llm-calorie-app
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart
sudo systemctl restart llm-calorie-app
```

**Update Ollama:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
sudo systemctl restart ollama
```

---

## Security Checklist

- [ ] Firewall configured (only necessary ports open)
- [ ] SSL/TLS enabled (HTTPS)
- [ ] Nginx reverse proxy setup
- [ ] API rate limiting (if needed)
- [ ] Authentication (if needed)
- [ ] Regular backups configured
- [ ] Monitoring and alerts setup
- [ ] Log rotation configured
- [ ] Regular security updates
- [ ] Strong passwords/keys

---

## Support

For issues or questions:
1. Check logs: `sudo journalctl -u llm-calorie-app -n 100`
2. Review [README.md](README.md)
3. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. Open an issue on GitHub

---

**Deployment complete! 🎉**

Your LLM Weight Loss Expert is now running in production.
