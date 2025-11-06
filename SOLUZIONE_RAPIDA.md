# ✅ Soluzione Rapida: Server WebSocket con ngrok

## 🔍 Il Problema

L'ESP32 si disconnette da `echo.websocket.org` perché:
- È un server **echo** (riflette solo i messaggi)
- **Non inoltra** messaggi tra client diversi
- Serve un server **intermedio** che inoltri i messaggi

## 🎯 La Soluzione

Usa il **server Python** che abbiamo creato + **ngrok** per esporlo su internet.

---

## 📋 Passi da Seguire

### 🖥️ IMPORTANTE: Quale Terminale Usare?

- **Terminale del Mac** (Terminal.app): Per server Python, ngrok, e client MacBook
- **Terminale di VS Code**: Per compilare/flashare ESP32 e monitor seriale

---

### 1️⃣ Installa ngrok (se non l'hai già)

**🖥️ Usa: Terminale del Mac** (Terminal.app)

Apri **Terminale** (trovalo in Applicazioni > Utility) e esegui:

```bash
brew install ngrok
```

Oppure scarica da: https://ngrok.com/download

### 2️⃣ Avvia il Server Python

**🖥️ Usa: Terminale del Mac** (Terminal.app)

**Apri un NUOVO terminale del Mac** (Terminal.app) e esegui:

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 server_websocket.py
```

⚠️ **IMPORTANTE**: 
- `source venv/bin/activate` attiva l'ambiente virtuale Python
- Devi farlo **ogni volta** che apri un nuovo terminale per eseguire il server
- Quando vedi `(venv)` all'inizio della riga, l'ambiente è attivo

Dovresti vedere:
```
============================================================
Server WebSocket per ESP32 <-> MacBook
============================================================
Server in ascolto su ws://0.0.0.0:8765
Premi Ctrl+C per fermare il server
============================================================
```

✅ **Lascia questo terminale aperto!**

### 3️⃣ Esponi il Server con ngrok

**🖥️ Usa: Terminale del Mac** (Terminal.app)

**Apri un ALTRO NUOVO terminale del Mac** (Terminal.app) e esegui:

```bash
ngrok http 8765
```

Dovresti vedere qualcosa come:
```
Forwarding   https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8765
```

📋 **COPIA l'URL** (esempio: `xxxx-xx-xx-xx-xx.ngrok-free.app`)

⚠️ **IMPORTANTE**: 
- ngrok usa **HTTPS** (non HTTP)
- L'URL sarà tipo: `xxxx-xx-xx-xx-xx.ngrok-free.app`
- **NON** includere `https://` nell'URL, solo il nome

### 4️⃣ Aggiorna ESP32

**💻 Usa: VS Code** (editor di testo)

Apri `src/main.cpp` in **VS Code** e modifica le righe 16-18:

**PRIMA:**
```cpp
const char* websocket_server = "echo.websocket.org";
const int websocket_port = 80;
const char* websocket_path = "/";
```

**DOPO** (sostituisci con il tuo URL ngrok):
```cpp
const char* websocket_server = "xxxx-xx-xx-xx-xx.ngrok-free.app";  // Il TUO URL ngrok
const int websocket_port = 443;  // HTTPS usa porta 443
const char* websocket_path = "/";
```

**Esempio reale:**
```cpp
const char* websocket_server = "a1b2c3d4e5f6.ngrok-free.app";
const int websocket_port = 443;
const char* websocket_path = "/";
```

### 5️⃣ Aggiorna MacBook

**💻 Usa: VS Code** (editor di testo)

Apri `macbook_client.py` in **VS Code** e modifica le righe 16-21:

**PRIMA:**
```python
WEBSOCKET_SERVER = "echo.websocket.org"
WEBSOCKET_PORT = 80
WEBSOCKET_PATH = "/"
WEBSOCKET_URL = f"ws://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

**DOPO** (sostituisci con il tuo URL ngrok):
```python
WEBSOCKET_SERVER = "xxxx-xx-xx-xx-xx.ngrok-free.app"  # Il TUO URL ngrok
WEBSOCKET_PORT = 443  # HTTPS usa porta 443
WEBSOCKET_PATH = "/"
# IMPORTANTE: usa wss:// per HTTPS (non ws://)
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

**Esempio reale:**
```python
WEBSOCKET_SERVER = "a1b2c3d4e5f6.ngrok-free.app"
WEBSOCKET_PORT = 443
WEBSOCKET_PATH = "/"
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

⚠️ **IMPORTANTE**: 
- Usa `wss://` (non `ws://`) perché ngrok usa HTTPS
- Porta `443` per HTTPS

### 6️⃣ Ricompila e Flasha ESP32

**💻 Usa: Terminale di VS Code** (o Terminale del Mac)

**Opzione A - Terminale di VS Code:**
1. Apri VS Code
2. Premi `Ctrl+`` (backtick) per aprire il terminale integrato
3. Oppure vai su **Terminal > New Terminal**
4. Esegui:

```bash
cd /Users/edoardocolella/ESP32_test
pio run -t upload -e esp32-audio-kit
```

**Opzione B - Terminale del Mac:**
1. Apri **Terminale** (Terminal.app)
2. Esegui:

```bash
cd /Users/edoardocolella/ESP32_test
pio run -t upload -e esp32-audio-kit
```

### 7️⃣ Apri il Monitor Seriale

**💻 Usa: Terminale di VS Code** (o Terminale del Mac)

**Opzione A - Terminale di VS Code:**
1. Nel terminale integrato di VS Code, esegui:

```bash
pio device monitor -b 115200 -p /dev/tty.usbserial-0001
```

**Opzione B - Terminale del Mac:**
1. Apri un **NUOVO terminale del Mac** (Terminal.app)
2. Esegui:

```bash
cd /Users/edoardocolella/ESP32_test
pio device monitor -b 115200 -p /dev/tty.usbserial-0001
```

Dovresti vedere:
```
[WebSocket] Connesso a: ...
```

✅ **Se vedi "Connesso" invece di "Disconnesso", funziona!**

### 8️⃣ Esegui il Client MacBook

**🖥️ Usa: Terminale del Mac** (Terminal.app)

**Apri un NUOVO terminale del Mac** (Terminal.app) e esegui:

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_client.py
```

⚠️ **IMPORTANTE**: 
- `source venv/bin/activate` attiva l'ambiente virtuale Python
- Devi farlo **ogni volta** che apri un nuovo terminale per eseguire il client
- Quando vedi `(venv)` all'inizio della riga, l'ambiente è attivo

Dovresti vedere:
```
✓ Connesso al server WebSocket!
```

### 9️⃣ Test Completo

1. **MacBook**: Digita un messaggio e premi INVIO
2. **ESP32**: Dovresti vedere il messaggio nel monitor seriale
3. **ESP32**: Invia automaticamente messaggi ogni 10 secondi
4. **MacBook**: Dovresti vedere i messaggi dall'ESP32

---

## 🎉 Funziona!

Ora ESP32 e MacBook possono comunicare in tempo reale!

---

## ⚠️ Note Importanti

### ngrok Gratuito
- L'URL **cambia** ogni volta che riavvii ngrok
- Devi **riaggiornare** ESP32 e MacBook con il nuovo URL
- Per URL fisso, usa ngrok a pagamento

### Server Python
- Deve essere **sempre in esecuzione**
- Se lo chiudi, ESP32 e MacBook si disconnettono

### ngrok
- Deve essere **sempre in esecuzione**
- Se lo chiudi, il server non è più accessibile da internet

---

## 🔄 Workflow Completo (4 Terminali)

### 🖥️ Terminali del Mac (Terminal.app):
1. **Terminale Mac 1**: `python3 server_websocket.py` (server)
2. **Terminale Mac 2**: `ngrok http 8765` (tunnel)
3. **Terminale Mac 3**: `python3 macbook_client.py` (client MacBook)

### 💻 Terminale di VS Code:
4. **Terminale VS Code**: Monitor seriale ESP32 (`pio device monitor`)
   - Oppure: Compila/flasha ESP32 (`pio run -t upload`)

---

## 📝 Riepilogo: Quale Terminale Usare?

| Operazione | Terminale da Usare |
|------------|-------------------|
| Installare ngrok | 🖥️ Terminale del Mac |
| Avviare server Python | 🖥️ Terminale del Mac |
| Avviare ngrok | 🖥️ Terminale del Mac |
| Eseguire client MacBook | 🖥️ Terminale del Mac |
| Compilare/flashare ESP32 | 💻 Terminale di VS Code (o Mac) |
| Monitor seriale ESP32 | 💻 Terminale di VS Code (o Mac) |
| Modificare file codice | 💻 VS Code (editor) |

---

## 🆘 Problemi?

### ESP32 si disconnette ancora
- Verifica che l'URL ngrok sia corretto
- Verifica che usi porta `443` (non `80`)
- Verifica che ngrok sia attivo

### MacBook non si connette
- Verifica che usi `wss://` (non `ws://`)
- Verifica che la porta sia `443`
- Verifica che ngrok sia attivo

### Messaggi non arrivano
- Verifica che il server Python sia in esecuzione
- Verifica che entrambi i client siano connessi
- Controlla i log del server Python

---

## 💡 Suggerimento

Per evitare di dover cambiare l'URL ogni volta, puoi:
1. **ngrok a pagamento**: URL fisso
2. **Server cloud**: Deploy su Heroku, Railway, etc. (vedi `COMUNICAZIONE_WEBSOCKET.md`)

