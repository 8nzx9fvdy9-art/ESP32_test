# 🚀 Soluzione Alternativa: Usa Render.com invece di ngrok

## Problema con ngrok
ngrok gratuito sta dando HTTP 404 per WebSocket. Questo è un problema comune con ngrok gratuito e WebSocket.

## Soluzione: Render.com (Gratuito, Supporta WebSocket)

Render è un servizio cloud gratuito che supporta WebSocket nativamente, senza problemi.

### Passo 1: Crea Account Render

1. Vai su https://render.com
2. Clicca "Get Started for Free"
3. Crea account (puoi usare GitHub)
4. È gratuito!

### Passo 2: Crea Nuovo Web Service

1. Nel dashboard Render, clicca "New +"
2. Seleziona "Web Service"
3. Connetti il tuo repository GitHub
   - Se non hai un repository, creane uno:
     ```bash
     cd /Users/edoardocolella/ESP32_test
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/TUO_USERNAME/ESP32_test.git
     git push -u origin main
     ```

### Passo 3: Configura il Deploy

1. **Name**: `websocket-server` (o qualsiasi nome)
2. **Environment**: `Python 3`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python3 server_render.py`
5. **Plan**: Free

### Passo 4: Deploy

1. Clicca "Create Web Service"
2. Render inizierà il deploy automaticamente
3. Aspetta 2-3 minuti per il deploy

### Passo 5: Ottieni l'URL

Dopo il deploy, Render ti darà un URL tipo:
```
https://websocket-server.onrender.com
```

### Passo 6: Aggiorna ESP32 e MacBook

**ESP32 (`src/main.cpp`):**
```cpp
const char* websocket_server = "websocket-server.onrender.com";  // Il TUO URL Render
const int websocket_port = 443;
```

**MacBook (`macbook_client.py`):**
```python
WEBSOCKET_SERVER = "websocket-server.onrender.com"  # Il TUO URL Render
WEBSOCKET_PORT = 443
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

---

## 🎯 Vantaggi di Render

✅ **Gratuito** (con limiti ragionevoli)  
✅ **Supporta WebSocket nativamente**  
✅ **HTTPS/WSS incluso** (certificati SSL validi)  
✅ **URL fisso** (non cambia)  
✅ **Nessun problema SSL** con ESP32  
✅ **Facile da usare** (deploy automatico da GitHub)  
✅ **Nessun problema HTTP 404** come ngrok

---

## 📝 File Necessari

Ho già creato:
- ✅ `server_render.py` - Server ottimizzato per Render
- ✅ `render.yaml` - Configurazione Render
- ✅ `requirements.txt` - Dipendenze Python (già esiste)

---

## 🔄 Workflow Completo con Render

1. **Crea account Render** (5 minuti)
2. **Crea repository GitHub** (se non ce l'hai)
3. **Connetti repository a Render** (2 minuti)
4. **Deploy automatico** (2-3 minuti)
5. **Ottieni URL** (es. `https://websocket-server.onrender.com`)
6. **Aggiorna ESP32 e MacBook** con l'URL Render
7. **Testa!**

---

## 🆘 Se Preferisci Continuare con ngrok

Se vuoi continuare con ngrok, il problema potrebbe essere:
1. ngrok gratuito ha limitazioni per WebSocket
2. Serve autenticazione ngrok (token)
3. Serve configurazione speciale

Ma Render è più semplice e funziona meglio!

