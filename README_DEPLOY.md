# 🚀 Deploy Server Render - Guida Rapida

## ⚡ Deploy Rapido (3 opzioni)

### Opzione 1: Deploy Automatico con API Key (PIÙ VELOCE)

```bash
# 1. Ottieni API key da: https://dashboard.render.com/account/api-keys
# 2. Esegui:
export RENDER_API_KEY='tua-api-key'
python3 deploy_render_api.py
```

### Opzione 2: Deploy con Render CLI

```bash
# 1. Installa CLI
brew install render

# 2. Login
render login

# 3. Deploy
python3 deploy_render.py
```

### Opzione 3: Deploy Manuale (SEMPRE FUNZIONA)

1. Vai su https://dashboard.render.com
2. Clicca **"New +"** > **"Web Service"**
3. Configura:
   - **Name**: `esp32-test-q46k`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
4. Carica file: `render_server.py`, `requirements.txt`, `Procfile`
5. Deploy!

---

## ✅ Verifica Deploy

```bash
curl https://esp32-test-q46k.onrender.com/status
```

Dovresti vedere:
```json
{"status": "online", ...}
```

---

## 📝 File Necessari

Tutti i file sono già pronti:
- ✅ `render_server.py`
- ✅ `requirements.txt`
- ✅ `Procfile`

---

## 🔗 Dettagli

Vedi `DEPLOY_ISTRUZIONI.md` per istruzioni dettagliate.

