# 🚀 Soluzione Alternativa: Usa Railway invece di ngrok

## Problema con ngrok
ngrok gratuito può avere problemi con WebSocket, specialmente con ESP32 e SSL.

## Soluzione: Railway (Gratuito, Facile, Supporta WebSocket)

Railway è un servizio cloud gratuito che supporta WebSocket nativamente, senza problemi SSL.

### Passo 1: Crea Account Railway

1. Vai su https://railway.app
2. Clicca "Login" e crea account (puoi usare GitHub)
3. È gratuito!

### Passo 2: Crea Nuovo Progetto

1. Clicca "New Project"
2. Seleziona "Deploy from GitHub repo"
3. Connetti il tuo repository GitHub (o crea uno nuovo)

### Passo 3: Configura il Deploy

Railway rileverà automaticamente che è un progetto Python e userà `server_websocket.py`.

**Oppure**, crea un file `Procfile` nella root del progetto:

```
web: python3 server_websocket.py
```

### Passo 4: Ottieni l'URL

Dopo il deploy, Railway ti darà un URL tipo:
```
https://tuo-progetto.up.railway.app
```

### Passo 5: Aggiorna ESP32 e MacBook

**ESP32 (`src/main.cpp`):**
```cpp
const char* websocket_server = "tuo-progetto.up.railway.app";
const int websocket_port = 443;
```

**MacBook (`macbook_client.py`):**
```python
WEBSOCKET_SERVER = "tuo-progetto.up.railway.app"
WEBSOCKET_PORT = 443
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

---

## 🎯 Vantaggi di Railway

✅ **Gratuito** (con limiti ragionevoli)  
✅ **Supporta WebSocket nativamente**  
✅ **HTTPS/WSS incluso** (certificati SSL validi)  
✅ **URL fisso** (non cambia come ngrok)  
✅ **Nessun problema SSL** con ESP32  
✅ **Facile da usare** (deploy automatico da GitHub)

---

## 🔄 Workflow Completo con Railway

1. **Crea account Railway** (5 minuti)
2. **Connetti repository GitHub** (2 minuti)
3. **Deploy automatico** (2 minuti)
4. **Ottieni URL** (es. `https://tuo-app.up.railway.app`)
5. **Aggiorna ESP32 e MacBook** con l'URL Railway
6. **Testa!**

---

## 💡 Alternativa: Test Locale con ngrok TCP

Se preferisci continuare con ngrok, prova un tunnel TCP:

```bash
ngrok tcp 8765
```

Poi usa la porta TCP fornita da ngrok (non 443).

---

## 🆘 Se Preferisci Continuare con ngrok

Il problema potrebbe essere che ngrok gratuito richiede autenticazione o ha limitazioni. Prova:

1. **Autentica ngrok:**
   ```bash
   ngrok config add-authtoken TUO_TOKEN
   ```
   (Ottieni il token da https://dashboard.ngrok.com/get-started/your-authtoken)

2. **Usa tunnel TCP:**
   ```bash
   ngrok tcp 8765
   ```

3. **Aggiorna ESP32** con la porta TCP fornita da ngrok

