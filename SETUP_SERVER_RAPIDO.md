# 🚀 Setup Server WebSocket Rapido con ngrok

## Problema
`echo.websocket.org` è un server echo che **riflette** i messaggi, ma **non inoltra** i messaggi tra client diversi. Per far comunicare ESP32 e MacBook, serve un server intermedio.

## Soluzione: Server Python + ngrok

### Passo 1: Installa ngrok

```bash
brew install ngrok
```

Oppure scarica da: https://ngrok.com/download

### Passo 2: Avvia il Server Python

In un terminale, esegui:

```bash
cd /Users/edoardocolella/ESP32_test
python3 server_websocket.py
```

Dovresti vedere:
```
Server WebSocket per ESP32 <-> MacBook
Server in ascolto su ws://0.0.0.0:8765
```

**Lascia questo terminale aperto!**

### Passo 3: Esponi il Server con ngrok

In un **NUOVO terminale**, esegui:

```bash
ngrok http 8765
```

Dovresti vedere qualcosa come:
```
Forwarding   https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8765
```

**Copia l'URL HTTPS** (esempio: `xxxx-xx-xx-xx-xx.ngrok-free.app`)

⚠️ **IMPORTANTE**: ngrok usa HTTPS, quindi l'URL sarà `wss://` (non `ws://`)

### Passo 4: Aggiorna ESP32

Apri `src/main.cpp` e modifica:

```cpp
const char* websocket_server = "xxxx-xx-xx-xx-xx.ngrok-free.app";  // Il tuo URL ngrok
const int websocket_port = 443;  // HTTPS usa porta 443
const char* websocket_path = "/";
```

**Oppure**, se ngrok ti dà un URL con porta specifica, usa quello.

### Passo 5: Aggiorna MacBook

Apri `macbook_client.py` e modifica:

```python
WEBSOCKET_SERVER = "xxxx-xx-xx-xx-xx.ngrok-free.app"  # Il tuo URL ngrok
WEBSOCKET_PORT = 443  # HTTPS usa porta 443
WEBSOCKET_PATH = "/"

# URL completo (usa wss:// per HTTPS)
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"
```

### Passo 6: Ricompila e Flasha ESP32

```bash
pio run -t upload -e esp32-audio-kit
```

### Passo 7: Test

1. **ESP32**: Dovrebbe connettersi al server ngrok
2. **MacBook**: Esegui `python3 macbook_client.py`
3. **Invia messaggi** da entrambi e verifica che arrivino!

---

## ⚠️ Note Importanti

- **ngrok gratuito**: L'URL cambia ogni volta che riavvii ngrok
- **ngrok a pagamento**: Puoi avere un URL fisso
- **Server locale**: Il server Python deve essere in esecuzione
- **ngrok attivo**: ngrok deve essere in esecuzione

---

## 🔄 Workflow Completo

1. **Terminale 1**: `python3 server_websocket.py` (server)
2. **Terminale 2**: `ngrok http 8765` (tunnel)
3. **Terminale 3**: Monitor seriale ESP32
4. **Terminale 4**: `python3 macbook_client.py` (client MacBook)

---

## 🆘 Problemi Comuni

### ngrok non si connette
- Verifica che il server Python sia in esecuzione
- Verifica che la porta 8765 sia libera

### ESP32 non si connette
- Verifica che l'URL ngrok sia corretto
- Verifica che usi `wss://` (non `ws://`) se ngrok usa HTTPS
- Verifica che la porta sia 443 per HTTPS

### Messaggi non arrivano
- Verifica che entrambi i client siano connessi
- Verifica i log del server Python
- Verifica che ngrok sia attivo

