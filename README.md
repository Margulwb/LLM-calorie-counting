# 🏋️ LLM Weight Loss Expert - AI-Powered Diet & Fitness Assistant

Kompletna aplikacja produkcyjna - LLM specjalista od odchudzania, liczenia kalorii, planowania diet i treningów. Wykorzystuje Ollama + Mistral 7B z systemem RAG do udzielania ekspertowych porad.

## ✨ Funkcje

### Backend API (Flask)
- 💬 **Diet Expert Chat** - Pytaj eksperta o dietę, trening, suplementację
- 📊 **Kalkulator Kalorii** - Obliczanie BMR, TDEE, deficytu kalorycznego
- 🍽️ **Generator Planów Posiłków** - Spersonalizowane plany żywieniowe
- 💪 **Generator Planów Treningowych** - Siła, cardio, lub połączenie
- 📈 **Analiza Postępów** - Co robić gdy waga stoi, optymalizacja

### LLM + RAG System
- 🤖 **Ollama + Mistral 7B** - Lokalny model językowy
- 📚 **Baza Wiedzy** - Kompleksowa wiedza o odchudzaniu
- 🔍 **RAG (Retrieval Augmented Generation)** - Precyzyjne odpowiedzi
- 🧠 **LangChain + ChromaDB** - Vector store dla wiedzy

### Frontend
- 🎨 **Prosty UI** - Interfejs do testowania wszystkich funkcji
- 📱 **Responsive** - Działa na desktop i mobile
- ⚡ **Real-time** - Natychmiastowe odpowiedzi

## 📋 Wymagania

### System
- Rocky Linux 9 / RHEL 9 / CentOS Stream 9 (lub Ubuntu/Debian)
- Python 3.9+
- 8GB RAM minimum (16GB zalecane dla Mistral 7B)
- ~10GB wolnego miejsca (model + dependencies)

### Wymagane pakiety
- curl
- gcc, g++, make
- git

## 🚀 Instalacja

### Opcja 1: Automatyczna instalacja (Rocky Linux 9)

```bash
# Sklonuj repozytorium
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting

# Uruchom skrypt instalacyjny (wymaga sudo)
sudo bash setup_rocky9.sh
```

Skrypt automatycznie:
- Zainstaluje Python 3.9+ i zależności systemowe
- Zainstaluje Ollama
- Pobierze model Mistral 7B
- Utworzy środowisko wirtualne Python
- Zainstaluje zależności Python
- Skonfiguruje systemd service
- Zainicjuje bazę wiedzy

### Opcja 2: Docker

```bash
# Zbuduj i uruchom
cd docker
docker-compose up -d

# Poczekaj aż Ollama pobierze model (pierwsze uruchomienie)
docker-compose logs -f ollama

# Sprawdź status
docker-compose ps
```

API dostępne pod: `http://localhost:5000`
Frontend dostępny pod: `http://localhost:8080`

### Opcja 3: Manualna instalacja

```bash
# 1. Zainstaluj Python 3.9+
sudo dnf install python3.9 python3.9-pip python3.9-devel -y

# 2. Zainstaluj Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 3. Uruchom Ollama
sudo systemctl start ollama
sudo systemctl enable ollama

# 4. Pobierz model Mistral
ollama pull mistral

# 5. Sklonuj repozytorium
git clone https://github.com/Margulwb/LLM-calorie-counting.git
cd LLM-calorie-counting

# 6. Utwórz środowisko wirtualne
python3.9 -m venv venv
source venv/bin/activate

# 7. Zainstaluj zależności
pip install --upgrade pip
pip install -r requirements.txt

# 8. Skopiuj i dostosuj konfigurację
cp .env.example .env
# Edytuj .env jeśli potrzeba

# 9. Uruchom aplikację
python backend/app.py
```

## 🎯 Użycie

### Uruchamianie serwera

**Z systemd (po automatycznej instalacji):**
```bash
# Uruchom
sudo systemctl start llm-calorie-app

# Status
sudo systemctl status llm-calorie-app

# Logi
sudo journalctl -u llm-calorie-app -f

# Stop
sudo systemctl stop llm-calorie-app
```

**Manualnie:**
```bash
cd /opt/llm-calorie-app  # lub ścieżka do repo
source venv/bin/activate
python backend/app.py
```

### Testowanie API

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Pytanie do eksperta:**
```bash
curl -X POST http://localhost:5000/api/diet-expert \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Ile białka powinienem jeść przy redukcji?",
    "context": {
      "weight": 80,
      "activity_level": "moderate"
    }
  }'
```

**Obliczenie kalorii:**
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

**Więcej przykładów:** Zobacz [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Interfejs Web

Otwórz w przeglądarce: `http://localhost:5000` lub `http://your-server-ip:5000`

Alternatywnie otwórz `frontend/index.html` bezpośrednio w przeglądarce.

## 📚 Dokumentacja

- **[API Documentation](API_DOCUMENTATION.md)** - Pełna dokumentacja API z przykładami
- **Knowledge Base** - Baza wiedzy w `knowledge_base/`:
  - `calories_macros.md` - Kalorie i makroskładniki
  - `caloric_deficit.md` - Deficyty kaloryczne i redukcja
  - `strength_vs_cardio.md` - Treningi siłowe vs cardio
  - `psychology.md` - Psychologia odchudzania
  - `supplements.md` - Suplementacja

## 🏗️ Struktura Projektu

```
LLM-calorie-counting/
├── backend/
│   ├── app.py                 # Główna aplikacja Flask
│   └── services/
│       ├── llm_service.py     # Serwis LLM + RAG
│       └── calculator_service.py  # Kalkulatory BMR/TDEE
├── frontend/
│   └── index.html             # Interfejs użytkownika
├── knowledge_base/
│   ├── calories_macros.md     # Baza wiedzy
│   ├── caloric_deficit.md
│   ├── strength_vs_cardio.md
│   ├── psychology.md
│   └── supplements.md
├── configs/
│   └── llm-calorie-app.service  # Systemd service
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── tests/                     # Testy (do dodania)
├── requirements.txt           # Zależności Python
├── setup_rocky9.sh           # Skrypt instalacyjny
├── .env.example              # Przykładowa konfiguracja
├── .gitignore
├── API_DOCUMENTATION.md
└── README.md
```

## 🔧 Konfiguracja

### Zmienne środowiskowe (.env)

```bash
# Flask
FLASK_ENV=production
PORT=5000

# Ollama
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434

# Logi
LOG_LEVEL=INFO
```

### Zmiana modelu LLM

Możesz użyć innych modeli wspieranych przez Ollama:

```bash
# Pobierz inny model
ollama pull llama2
# lub
ollama pull codellama

# Zaktualizuj .env
OLLAMA_MODEL=llama2
```

## 🔐 Bezpieczeństwo

### Dla produkcji:
1. **Firewall:** Ogranicz dostęp do portu 5000
2. **Reverse Proxy:** Użyj Nginx/Apache z SSL
3. **Authentication:** Dodaj API keys lub OAuth2
4. **Rate Limiting:** Ogranicz liczbę requestów
5. **CORS:** Skonfiguruj konkretne dozwolone originy

### Przykład Nginx z SSL:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitorowanie

### Logi systemd:
```bash
# Ostatnie logi
sudo journalctl -u llm-calorie-app -n 100

# Logi na żywo
sudo journalctl -u llm-calorie-app -f

# Logi z ostatniej godziny
sudo journalctl -u llm-calorie-app --since "1 hour ago"
```

### Status usług:
```bash
# Status aplikacji
sudo systemctl status llm-calorie-app

# Status Ollama
sudo systemctl status ollama

# Sprawdź czy Ollama działa
curl http://localhost:11434/api/version
```

## 🐛 Troubleshooting

### Ollama nie odpowiada
```bash
# Restart Ollama
sudo systemctl restart ollama

# Sprawdź logi
sudo journalctl -u ollama -n 50
```

### Model nie został pobrany
```bash
# Sprawdź dostępne modele
ollama list

# Pobierz Mistral
ollama pull mistral
```

### Błędy z ChromaDB
```bash
# Usuń i zainicjuj ponownie
rm -rf chroma_db/
python -c "from backend.services.llm_service import LLMService; LLMService()"
```

### Porty już zajęte
```bash
# Sprawdź co używa portu 5000
sudo lsof -i :5000

# Zmień port w .env
PORT=5001
```

## 🧪 Testowanie

```bash
# Uruchom testy (gdy zostaną dodane)
source venv/bin/activate
pytest tests/

# Lub manualnie testuj endpoints
python tests/manual_test.py
```

## 📈 Performance

### Typowe czasy odpowiedzi:
- Health check: ~10ms
- Kalkulacje: ~50ms
- Generowanie z LLM: 2-10s (zależnie od modelu i hardware)
- Pierwsze zapytanie (inicjalizacja): ~30s

### Optymalizacja:
- Użyj GPU dla Ollama (znacznie szybsze)
- Użyj mniejszego modelu (mistral:7b-instruct-q4_0)
- Zwiększ RAM dla cache'owania modelu

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Ten projekt jest otwarty na użytek osobisty i edukacyjny.

## 👨‍💻 Autor

Stworzony dla społeczności fitness i health tech.

## 🙏 Podziękowania

- **Ollama** - Lokalny LLM runtime
- **Mistral AI** - Model językowy
- **LangChain** - Framework RAG
- **Flask** - Web framework

## 📞 Wsparcie

Jeśli masz problemy:
1. Sprawdź [Issues](https://github.com/Margulwb/LLM-calorie-counting/issues)
2. Przeczytaj dokumentację API
3. Sprawdź logi systemd
4. Otwórz nowy Issue z opisem problemu

## 🔄 Aktualizacje

```bash
# Zaktualizuj kod
git pull origin main

# Zaktualizuj zależności
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart usługi
sudo systemctl restart llm-calorie-app
```

---

**Status projektu:** ✅ Production Ready

**Ostatnia aktualizacja:** 2024
