# 🔧 Troubleshooting: Errore SSL con ngrok

## Problema
```
[E][ssl_client.cpp:37] _handle_error(): [start_ssl_client():273]: (-29312) SSL - The connection indicated an EOF
[E][WiFiClientSecure.cpp:144] connect(): start_ssl_client: -29312
[WebSocket] Disconnesso
```

## Possibili Cause

### 1. Server Python non è in esecuzione
**Verifica:**
- Apri il terminale dove hai avviato il server Python
- Dovresti vedere: `Server in ascolto su ws://0.0.0.0:8765`
- Se NON vedi questo, avvia il server!

### 2. ngrok non è in esecuzione
**Verifica:**
- Apri il terminale dove hai avviato ngrok
- Dovresti vedere: `Forwarding https://... -> http://localhost:8765`
- Se NON vedi questo, avvia ngrok!

### 3. ngrok gratuito ha limitazioni per WebSocket
**Soluzione:**
ngrok gratuito potrebbe avere problemi con WebSocket. Prova:

**Opzione A: Usa ngrok con upgrade WebSocket esplicito**
```bash
ngrok http 8765 --request-header-add "Upgrade: websocket"
```

**Opzione B: Usa tunnel TCP invece di HTTP**
```bash
ngrok tcp 8765
```
Poi usa la porta TCP fornita da ngrok (non 443).

**Opzione C: Usa un servizio cloud gratuito**
- Heroku (gratuito)
- Railway (gratuito)
- Render (gratuito)

### 4. Problema con certificati SSL
**Soluzione:**
Ho già configurato `beginSSL` senza fingerprint per accettare qualsiasi certificato.

## ✅ Checklist di Verifica

1. **Server Python in esecuzione?**
   ```bash
   # Terminale Mac 1
   cd /Users/edoardocolella/ESP32_test
   source venv/bin/activate
   python3 server_websocket.py
   ```
   ✅ Dovresti vedere: `Server in ascolto su ws://0.0.0.0:8765`

2. **ngrok in esecuzione?**
   ```bash
   # Terminale Mac 2
   ngrok http 8765
   ```
   ✅ Dovresti vedere: `Forwarding https://... -> http://localhost:8765`

3. **URL ngrok corretto in ESP32?**
   - Apri `src/main.cpp`
   - Verifica: `websocket_server = "nonflatulent-colby-pearly.ngrok-free.dev"`
   - Verifica: `websocket_port = 443`

4. **URL ngrok corretto in MacBook?**
   - Apri `macbook_client.py`
   - Verifica: `WEBSOCKET_SERVER = "nonflatulent-colby-pearly.ngrok-free.dev"`
   - Verifica: `WEBSOCKET_PORT = 443`
   - Verifica: `WEBSOCKET_URL = f"wss://..."`

## 🔄 Prossimi Passi

### Prova 1: Verifica che il server Python riceva connessioni

Quando l'ESP32 tenta di connettersi, dovresti vedere nel terminale del server Python:
```
[HH:MM:SS] Nuovo client connesso. Totale: 1
```

**Se NON vedi questo**, il problema è che ngrok non sta inoltrando le connessioni al server Python.

### Prova 2: Testa con il client MacBook

Esegui il client MacBook:
```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_client.py
```

**Se il MacBook si connette ma l'ESP32 no**, il problema è specifico dell'ESP32/SSL.

### Prova 3: Usa un servizio cloud alternativo

Se ngrok continua a dare problemi, considera:
- **Heroku**: Gratuito, supporta WebSocket nativamente
- **Railway**: Gratuito, facile da usare
- **Render**: Gratuito, supporta WebSocket

## 💡 Soluzione Alternativa: Usa HTTP invece di HTTPS

Se ngrok continua a dare problemi con SSL, potresti:
1. Usare un servizio che supporta HTTP (non sicuro, solo per test)
2. O configurare ngrok per usare HTTP (ma ngrok gratuito usa sempre HTTPS)

## 🆘 Se Nulla Funziona

Considera di usare un servizio cloud gratuito come Heroku o Railway che supporta WebSocket nativamente senza problemi SSL.

