# ✅ Verifica Setup - Checklist

## 🔍 Prima di tutto: Verifica che tutto sia in esecuzione

### 1. Server Python deve essere in esecuzione

**🖥️ Terminale Mac 1** - Dovresti vedere:

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 server_websocket.py
```

**Output atteso:**
```
============================================================
Server WebSocket per ESP32 <-> MacBook
============================================================
Server in ascolto su ws://0.0.0.0:8765
Premi Ctrl+C per fermare il server
============================================================
```

✅ **Se vedi questo, il server è attivo!**

❌ **Se NON vedi questo, avvia il server!**

---

### 2. ngrok deve essere in esecuzione

**🖥️ Terminale Mac 2** - Dovresti vedere:

```bash
ngrok http 8765
```

**Output atteso:**
```
Forwarding   https://nonflatulent-colby-pearly.ngrok-free.dev -> http://localhost:8765
```

✅ **Se vedi questo, ngrok è attivo!**

❌ **Se NON vedi questo, avvia ngrok!**

---

### 3. ESP32 deve essere configurato correttamente

**💻 VS Code** - Apri `src/main.cpp` e verifica:

```cpp
const char* websocket_server = "nonflatulent-colby-pearly.ngrok-free.dev";
const int websocket_port = 443;
```

✅ **Se è così, è corretto!**

❌ **Se è diverso, aggiorna con l'URL ngrok corretto!**

---

### 4. Client MacBook deve essere configurato correttamente

**💻 VS Code** - Apri `macbook_client.py` e verifica:

```python
WEBSOCKET_SERVER = "nonflatulent-colby-pearly.ngrok-free.dev"
WEBSOCKET_PORT = 443
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

✅ **Se è così, è corretto!**

❌ **Se è diverso, aggiorna con l'URL ngrok corretto!**

---

## 🚀 Prossimi Passi

### 1. Ricompila e Flasha ESP32

**💻 Terminale VS Code:**

```bash
cd /Users/edoardocolella/ESP32_test
pio run -t upload -e esp32-audio-kit
```

### 2. Apri Monitor Seriale

**💻 Terminale VS Code:**

```bash
pio device monitor -b 115200 -p /dev/tty.usbserial-0001
```

**Dovresti vedere:**
```
WiFi connesso!
IP address: 192.168.0.85
Tentativo di connessione a WebSocket server: nonflatulent-colby-pearly.ngrok-free.dev:443
[WebSocket] Connesso a: ...
```

✅ **Se vedi "Connesso", funziona!**

❌ **Se vedi "Disconnesso", verifica:**
- Server Python è in esecuzione?
- ngrok è in esecuzione?
- URL ngrok è corretto?

### 3. Esegui Client MacBook

**🖥️ Terminale Mac 3:**

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_client.py
```

**Dovresti vedere:**
```
✓ Connesso al server WebSocket!
```

✅ **Se vedi questo, funziona!**

---

## 🆘 Problemi Comuni

### ESP32 si disconnette continuamente

**Possibili cause:**
1. Server Python non è in esecuzione
2. ngrok non è in esecuzione
3. URL ngrok non è corretto
4. ESP32 non supporta WSS (ho aggiunto `beginSSL` per risolvere questo)

**Soluzioni:**
1. Verifica che il server Python sia in esecuzione (Terminale Mac 1)
2. Verifica che ngrok sia in esecuzione (Terminale Mac 2)
3. Verifica che l'URL ngrok sia corretto in `src/main.cpp`
4. Ricompila e flasha l'ESP32 con il nuovo codice (include `beginSSL`)

### Client MacBook non si connette

**Possibili cause:**
1. Server Python non è in esecuzione
2. ngrok non è in esecuzione
3. URL ngrok non è corretto
4. Ambiente virtuale Python non è attivo

**Soluzioni:**
1. Verifica che il server Python sia in esecuzione
2. Verifica che ngrok sia in esecuzione
3. Verifica che l'URL ngrok sia corretto in `macbook_client.py`
4. Attiva l'ambiente virtuale: `source venv/bin/activate`

---

## ✅ Checklist Finale

- [ ] Server Python in esecuzione (Terminale Mac 1)
- [ ] ngrok in esecuzione (Terminale Mac 2)
- [ ] ESP32 configurato con URL ngrok corretto
- [ ] Client MacBook configurato con URL ngrok corretto
- [ ] ESP32 ricompilato e flashato con supporto WSS (`beginSSL`)
- [ ] Monitor seriale ESP32 mostra "Connesso"
- [ ] Client MacBook mostra "Connesso"

Se tutti questi sono ✅, la comunicazione dovrebbe funzionare!

