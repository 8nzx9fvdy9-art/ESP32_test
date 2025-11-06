# Comunicazione Full-Duplex ESP32 ↔ MacBook M2 via WebSocket

Questa guida spiega come far comunicare un ESP32 con un MacBook M2 su reti WiFi diverse usando WebSocket.

## Architettura

```
ESP32 (WiFi A)  ←→  [Server WebSocket]  ←→  MacBook M2 (WiFi B)
```

Il server WebSocket funge da intermediario, permettendo la comunicazione bidirezionale anche se i dispositivi sono su reti diverse.

## Opzioni per il Server WebSocket

### Opzione 1: Server Pubblico (per test)
Usa un servizio pubblico come `echo.websocket.org` per test rapidi.

**Vantaggi**: Nessuna configurazione necessaria  
**Svantaggi**: Non sicuro, solo per test, tutti i messaggi sono pubblici

### Opzione 2: Server Proprio Locale (con ngrok)
Esegui il server su MacBook e usa ngrok per esporlo su internet.

**Passi**:
1. Installa ngrok: `brew install ngrok` o da https://ngrok.com
2. Esegui il server: `python3 server_websocket.py`
3. In un altro terminale: `ngrok http 8765`
4. Copia l'URL HTTPS fornito da ngrok (es. `wss://xxxx.ngrok.io`)
5. Usa questo URL nell'ESP32 e nel client MacBook

### Opzione 3: Server Cloud (Produzione)
Deploy su servizi cloud come:
- **Heroku**: Gratuito per test
- **Railway**: Facile da usare
- **DigitalOcean**: VPS economico
- **AWS EC2**: Più complesso ma potente

## Setup ESP32

### 1. Configura WiFi

Modifica `src/websocket_client.cpp`:

```cpp
const char* ssid = "NOME_RETE_WIFI";
const char* password = "PASSWORD_WIFI";
```

### 2. Configura Server WebSocket

```cpp
const char* websocket_server = "tuo-server.com";  // o IP pubblico
const int websocket_port = 8765;  // o porta del tuo server
const char* websocket_path = "/";
```

### 3. Aggiungi libreria WebSocket

Aggiungi al `platformio.ini`:

```ini
lib_deps = 
  https://github.com/pschatzmann/arduino-audiokit.git
  earlephilhower/ESP8266Audio@^1.9.9
  links2004/WebSockets@^2.4.1
```

### 4. Compila e Flasha

```bash
pio run -t upload -e esp32-audio-kit
```

## Setup MacBook M2

### 1. Installa dipendenze Python

```bash
pip3 install websockets
```

Oppure:

```bash
pip3 install -r requirements.txt
```

### 2. Esegui il Client

```bash
python3 macbook_client.py
```

### 3. Configura Server

Modifica `WEBSOCKET_SERVER` in `macbook_client.py` per puntare al tuo server.

## Setup Server Intermedio (Opzione 2/3)

### Server Locale con ngrok

1. **Installa ngrok**:
   ```bash
   brew install ngrok
   # oppure scarica da https://ngrok.com
   ```

2. **Esegui il server**:
   ```bash
   python3 server_websocket.py
   ```

3. **Esponi con ngrok** (in un altro terminale):
   ```bash
   ngrok http 8765
   ```

4. **Copia l'URL** fornito da ngrok (es. `wss://xxxx-xx-xx-xx-xx.ngrok-free.app`)

5. **Aggiorna ESP32 e MacBook** con questo URL

### Deploy su Heroku

1. **Crea account Heroku** e installa Heroku CLI

2. **Crea file `Procfile`**:
   ```
   web: python3 server_websocket.py
   ```

3. **Crea file `runtime.txt`**:
   ```
   python-3.11.0
   ```

4. **Deploy**:
   ```bash
   heroku create tuo-nome-app
   git push heroku main
   ```

5. **Ottieni URL**: `wss://tuo-nome-app.herokuapp.com`

## Test della Comunicazione

### Test Base

1. **ESP32**: Dovrebbe connettersi e inviare messaggi ogni 10 secondi
2. **MacBook**: Esegui `python3 macbook_client.py`
3. **Digita un messaggio** nel terminale MacBook e premi INVIO
4. **Verifica** che l'ESP32 riceva il messaggio sulla seriale

### Test Avanzato

- **Invio da ESP32**: Scrivi sulla seriale dell'ESP32, il messaggio arriverà al MacBook
- **Invio da MacBook**: Digita nel terminale Python, il messaggio arriverà all'ESP32
- **Full-Duplex**: Entrambi possono inviare e ricevere simultaneamente

## Sicurezza

⚠️ **Importante**: Per uso in produzione:

1. **Usa WSS (WebSocket Secure)** invece di WS
2. **Aggiungi autenticazione** (token, API key)
3. **Cripta i messaggi** se contengono dati sensibili
4. **Usa un server con certificato SSL valido**

## Troubleshooting

### ESP32 non si connette al WiFi
- Verifica SSID e password
- Controlla che la rete WiFi sia 2.4GHz (ESP32 non supporta 5GHz)

### Errore di connessione WebSocket
- Verifica che il server sia raggiungibile
- Controlla firewall e porte
- Per ngrok, assicurati che il tunnel sia attivo

### Messaggi non arrivano
- Verifica che entrambi i client siano connessi al server
- Controlla i log del server
- Assicurati che il server inoltri correttamente i messaggi

## Esempi di Uso

### Controllo Remoto
- MacBook invia comandi all'ESP32
- ESP32 esegue azioni (accendi LED, riproduci audio, etc.)

### Monitoraggio
- ESP32 invia dati sensori al MacBook
- MacBook visualizza grafici in tempo reale

### Chat Bidirezionale
- Comunicazione testuale tra ESP32 e MacBook
- Messaggi in tempo reale

## Note

- Il server intermedio è necessario perché ESP32 e MacBook sono su reti diverse
- WebSocket supporta full-duplex nativamente
- La latenza dipende dalla distanza dal server intermedio
- Per latenze minime, usa un server geograficamente vicino

