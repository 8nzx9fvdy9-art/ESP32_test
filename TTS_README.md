# Sistema Text-to-Speech (TTS) per ESP32-A1S

Sistema completo per inviare testo dal MacBook e riprodurlo come voce sull'ESP32-A1S tramite Google TTS.

## Architettura

```
MacBook (Python + gTTS)  -->  [Genera MP3]  -->  [Upload a server]  -->  ESP32 (HTTP Server)  -->  [Riproduce audio via I2S]
```

## Componenti

1. **ESP32 Server** (`tts_server_example.c`): Server HTTP sull'ESP32 che riceve URL audio e li riproduce
2. **Python Client** (`tts_client.py`): Script Python che genera audio con gTTS e lo invia all'ESP32

## Configurazione ESP32

### 1. Compilare il firmware TTS Server

Modifica `main/CMakeLists.txt`:

```cmake
# Cambia questa riga:
set(COMPONENT_SRCS ./tts_server_example.c)
```

### 2. Configurare WiFi

Esegui `idf.py menuconfig` e configura:

```
Component config → TTS Server Configuration
  WiFi SSID: [il tuo SSID]
  WiFi Password: [la tua password]
```

Oppure modifica `sdkconfig` direttamente:

```ini
CONFIG_WIFI_SSID="il_tuo_ssid"
CONFIG_WIFI_PASSWORD="la_tua_password"
```

### 3. Compilare e flashare

```bash
idf.py build
idf.py flash monitor
```

L'ESP32 stamperà l'indirizzo IP quando si connette al WiFi:
```
WiFi connected! IP address: 192.168.1.100
TTS Server ready! Send POST requests to http://192.168.1.100/play
```

## Configurazione MacBook

### 1. Installare dipendenze Python

```bash
pip install gtts requests
```

### 2. Configurare lo script

Modifica `tts_client.py` se necessario (IP di default, lingua, ecc.):

```python
DEFAULT_ESP32_IP = "192.168.1.100"  # Cambia con l'IP del tuo ESP32
DEFAULT_LANG = "it"  # Lingua (it=italiano, en=inglese, ecc.)
```

### 3. Rendere eseguibile

```bash
chmod +x tts_client.py
```

## Utilizzo

### Modalità semplice (singolo comando)

```bash
python tts_client.py "Ciao, questo è un test di sintesi vocale"
```

### Modalità interattiva

```bash
python tts_client.py --interactive
```

Poi inserisci il testo quando richiesto.

### Opzioni avanzate

```bash
# Specifica IP ESP32
python tts_client.py --esp32-ip 192.168.1.50 "Hello world"

# Cambia lingua
python tts_client.py --lang en "Hello world"

# Usa file audio esistente
python tts_client.py --audio-file http://example.com/audio.mp3
```

## API Endpoints

### POST /play
Riproduci audio da URL

**Request:**
```json
{
  "url": "http://example.com/audio.mp3"
}
```

**Oppure query parameter:**
```
POST /play?url=http://example.com/audio.mp3
```

**Response:**
```json
{
  "status": "playing",
  "message": "Audio playback started"
}
```

### POST /text
Ricevi testo (per uso futuro con TTS su ESP32)

**Request:**
```json
{
  "text": "Testo da pronunciare"
}
```

### GET /
Pagina HTML con informazioni sul server

## Funzionamento

1. **Generazione Audio**: Lo script Python usa `gTTS` per generare un file MP3 dal testo
2. **Upload**: Il file MP3 viene caricato su un servizio di file sharing (transfer.sh) per ottenere un URL pubblico
3. **Invio all'ESP32**: L'URL viene inviato all'ESP32 tramite POST request
4. **Riproduzione**: L'ESP32 scarica l'audio dall'URL e lo riproduce tramite I2S

## Limitazioni e Note

- **Servizio di Hosting**: Lo script usa `transfer.sh` per hosting temporaneo. Per produzione, usa un server stabile
- **Lunghezza Testo**: Google TTS ha limiti sulla lunghezza del testo (circa 5000 caratteri)
- **Connessione Internet**: Sia MacBook che ESP32 devono essere connessi a Internet
- **Latenza**: C'è una latenza dovuta alla generazione audio e upload (circa 2-5 secondi)

## Alternative per Hosting Audio

### Opzione 1: Server HTTP locale con ngrok

```bash
# Sul MacBook, avvia un server HTTP
python -m http.server 8000

# In un altro terminale, espone con ngrok
ngrok http 8000

# Usa l'URL ngrok nell'ESP32
```

### Opzione 2: Server web personale

Carica il file MP3 sul tuo server web e invia l'URL all'ESP32.

### Opzione 3: Google Cloud Storage / AWS S3

Per produzione, usa un servizio cloud per hosting file.

## Troubleshooting

### ESP32 non si connette al WiFi
- Verifica SSID e password in `menuconfig`
- Controlla che la rete WiFi sia a 2.4GHz (ESP32 non supporta 5GHz)

### Errore "Connection refused"
- Verifica che l'IP dell'ESP32 sia corretto
- Controlla che l'ESP32 sia connesso al WiFi (vedi log seriale)
- Verifica che il firewall non blocchi la porta 80

### Audio non si sente
- Verifica che le cuffie/speaker siano collegati correttamente
- Controlla il volume sul codec (ES8388)
- Verifica che l'URL audio sia accessibile dall'ESP32

### Errore gTTS
- Verifica connessione Internet sul MacBook
- Alcune lingue potrebbero richiedere TLD diverso (usa `--tld`)

## Sviluppi Futuri

- [ ] Integrazione diretta con Google Cloud TTS API sull'ESP32
- [ ] Supporto per più lingue e voci
- [ ] Cache locale degli audio generati
- [ ] Interfaccia web per inviare testo
- [ ] Supporto per SSML (Speech Synthesis Markup Language)

## Licenza

Questo esempio è rilasciato nel pubblico dominio (CC0).


