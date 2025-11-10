# 🚀 Istruzioni Deploy Server Render

## ✅ File Pronti

Tutti i file necessari sono già presenti:
- ✅ `render_server.py` - Server Flask
- ✅ `requirements.txt` - Dipendenze Python
- ✅ `Procfile` - Configurazione Render

## 🎯 Opzione 1: Deploy Automatico (CLI)

### 1. Installa Render CLI

```bash
brew install render
```

### 2. Login

```bash
render login
```

### 3. Deploy

```bash
python3 deploy_render.py
```

Oppure manualmente:

```bash
render services create web \
  --name esp32-test-q46k \
  --env python \
  --buildCommand "pip install -r requirements.txt" \
  --startCommand "gunicorn render_server:app --bind 0.0.0.0:\$PORT --workers 2 --threads 2 --timeout 120" \
  --region oregon \
  --plan free
```

---

## 🎯 Opzione 2: Deploy via GitHub

### 1. Crea Repository GitHub

```bash
# Inizializza git (se non già fatto)
git init
git add render_server.py requirements.txt Procfile
git commit -m "Render server for ESP32 audio streaming"
git remote add origin <URL_TUO_REPO>
git push -u origin main
```

### 2. Deploy su Render

1. Vai su https://dashboard.render.com
2. Clicca **"New +"** > **"Web Service"**
3. Collega il tuo repository GitHub
4. Configurazione:
   - **Name**: `esp32-test-q46k`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
   - **Plan**: `Free`
5. Clicca **"Create Web Service"**

---

## 🎯 Opzione 3: Deploy Manuale (Upload)

### 1. Vai su Render Dashboard

https://dashboard.render.com

### 2. Crea Nuovo Servizio

1. Clicca **"New +"** > **"Web Service"**
2. Seleziona **"Public Git repository"** o **"Private Git repository"**
3. Oppure usa **"Manual Deploy"**

### 3. Configurazione

- **Name**: `esp32-test-q46k`
- **Environment**: `Python 3`
- **Region**: `Oregon` (o più vicino a te)
- **Branch**: `main` (o `master`)
- **Root Directory**: `/` (root)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
- **Plan**: `Free`

### 4. Carica File

Se usi Manual Deploy, carica:
- `render_server.py`
- `requirements.txt`
- `Procfile`

### 5. Deploy

Clicca **"Create Web Service"** e attendi il deploy (2-5 minuti)

---

## ✅ Verifica Deploy

Dopo il deploy, verifica che il server sia online:

```bash
curl https://esp32-test-q46k.onrender.com/status
```

Dovresti vedere:
```json
{
  "status": "online",
  "buffer_size": 0,
  "stream_active": false,
  "last_audio_time": null
}
```

---

## 🔧 Troubleshooting

### Server non risponde

1. Controlla i log su Render Dashboard
2. Verifica che tutti i file siano presenti
3. Controlla che il `Procfile` sia corretto

### Errore SSL nell'ESP32

Se vedi errori SSL nell'ESP32, il server Render usa HTTPS di default. 
L'ESP32 dovrebbe gestire HTTPS automaticamente, ma se ci sono problemi:

1. Verifica che l'URL sia corretto: `https://esp32-test-q46k.onrender.com`
2. Controlla i log ESP32 per errori SSL specifici
3. Il server Render fornisce automaticamente certificati SSL validi

### Server si spegne dopo 15 minuti

- Il piano gratuito di Render spegne i servizi dopo 15 minuti di inattività
- Per mantenerlo attivo, considera un piano a pagamento
- Oppure usa un servizio di ping periodico

---

## 📝 Note

- Il primo deploy può richiedere 5-10 minuti
- I deploy successivi sono più veloci (2-3 minuti)
- Il server Render fornisce automaticamente HTTPS
- L'URL sarà: `https://esp32-test-q46k.onrender.com`

---

## 🎉 Fatto!

Una volta deployato, l'URL sarà:
**https://esp32-test-q46k.onrender.com**

Configura questo URL nell'ESP32 usando `menuconfig` o `configure_render.sh`

