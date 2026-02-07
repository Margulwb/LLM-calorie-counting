# 🚀 Quick Start Guide

## Installation (Choose One Method)

### Option 1: Automated (Rocky Linux 9) - RECOMMENDED
```bash
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting
sudo bash setup_rocky9.sh
```
**Time: ~15-20 minutes** (includes model download)

### Option 2: Docker - EASIEST
```bash
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting/docker
docker-compose up -d
```
**Time: ~10-15 minutes** (first run)

### Option 3: Manual
See [README.md](README.md#opcja-3-manualna-instalacja) for step-by-step instructions.

---

## Quick Test

### 1. Health Check
```bash
curl http://localhost:5000/health
```
**Expected:** `{"status":"healthy",...}`

### 2. Calculate Calories
```bash
curl -X POST http://localhost:5000/api/calculate-deficit \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 80,
    "height": 180,
    "age": 30,
    "gender": "male",
    "activity_level": "moderate",
    "goal": "weight_loss"
  }'
```

### 3. Ask Expert
```bash
curl -X POST http://localhost:5000/api/diet-expert \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Ile białka powinienem jeść?"
  }'
```

### 4. Open Web UI
Open browser: `http://localhost:5000` or `http://your-server-ip:5000`

---

## Common Commands

### Service Management (systemd)
```bash
# Start
sudo systemctl start llm-calorie-app

# Stop
sudo systemctl stop llm-calorie-app

# Restart
sudo systemctl restart llm-calorie-app

# Status
sudo systemctl status llm-calorie-app

# Logs
sudo journalctl -u llm-calorie-app -f
```

### Docker
```bash
# Start
cd docker && docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart
```

---

## File Locations

### Application Files
- **App:** `/opt/llm-calorie-app/` (or your clone location)
- **Config:** `/opt/llm-calorie-app/.env`
- **Logs:** `journalctl -u llm-calorie-app` (systemd)
- **Vector DB:** `/opt/llm-calorie-app/chroma_db/`

### Service Files
- **Systemd:** `/etc/systemd/system/llm-calorie-app.service`
- **Nginx:** `/etc/nginx/conf.d/llm-calorie-app.conf` (if using)

---

## Troubleshooting

### Problem: API not responding
```bash
# Check if service is running
sudo systemctl status llm-calorie-app

# Check if Ollama is running
sudo systemctl status ollama

# Restart both
sudo systemctl restart ollama
sudo systemctl restart llm-calorie-app
```

### Problem: Port 5000 in use
```bash
# Find what's using the port
sudo lsof -i :5000

# Change port in .env
echo "PORT=5001" >> .env
sudo systemctl restart llm-calorie-app
```

### Problem: Ollama model not found
```bash
# List installed models
ollama list

# Pull Mistral
ollama pull mistral
```

### Problem: Slow responses
- **First time?** Vector DB initialization takes ~30s
- **Low RAM?** Mistral needs ~8GB RAM
- **CPU only?** Consider using GPU or smaller model:
  ```bash
  ollama pull mistral:7b-instruct-q4_0
  ```

---

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/diet-expert` | POST | Ask nutrition expert |
| `/api/calculate-deficit` | POST | Calculate calories & macros |
| `/api/meal-plan` | POST | Generate meal plan |
| `/api/workout-plan` | POST | Generate workout plan |
| `/api/analyze-progress` | POST | Analyze weight loss progress |

**Full docs:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## Production Checklist

Before deploying to production:

- [ ] Change default ports if needed (`.env`)
- [ ] Setup Nginx reverse proxy ([DEPLOYMENT.md](DEPLOYMENT.md))
- [ ] Enable SSL/HTTPS
- [ ] Configure firewall
- [ ] Setup monitoring and alerts
- [ ] Configure backups
- [ ] Test all endpoints
- [ ] Setup log rotation
- [ ] Consider authentication
- [ ] Review security settings

**Full guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Need Help?

1. **Check logs:**
   ```bash
   sudo journalctl -u llm-calorie-app -n 100
   ```

2. **Read docs:**
   - [README.md](README.md) - Setup & usage
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment

3. **Open issue:**
   https://github.com/Margulwb/LLM-calorie-counting/issues

---

## Quick Reference

### Environment Variables
```bash
FLASK_ENV=production        # production or development
PORT=5000                   # API port
OLLAMA_MODEL=mistral        # LLM model name
OLLAMA_HOST=http://localhost:11434  # Ollama URL
```

### Default Settings
- **API Port:** 5000
- **Ollama Port:** 11434
- **Model:** mistral (7B)
- **Language:** Polish
- **Min Calories:** 1200 (female), 1500 (male)

### Performance
- Health check: ~10ms
- Calculations: ~50ms
- LLM responses: 2-10s
- First request: ~30s (initialization)

---

**Status:** ✅ Production Ready
**Version:** 1.0.0
**Last Updated:** 2024

---

**Pro Tip:** Bookmark this file for quick command reference! 🔖
