# 🎵 Streaming Audio MacBook -> ESP32 via Render

Questa soluzione permette di trasmettere l'audio del MacBook all'uscita jack dell'ESP32, anche se i due dispositivi sono su reti internet diverse, usando Render come intermediario.

## 📋 Architettura

```
MacBook (audio di sistema) 
    ↓ (POST /audio)
Server Render (intermediario)
    ↓ (GET /stream)
ESP32 (riproduce su jack)
```

## 🚀 Setup Server Render

### 1. Crea un account su Render

1. Vai su [render.com](https://render.com)
2. Crea un account gratuito
3. Crea un nuovo "Web Service"

### 2. Configura il servizio su Render

1. **Repository**: Collega il tuo repository GitHub o carica i file manualmente
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
4. **Environment**: Render imposta automaticamente `PORT`

### 3. File necessari su Render

Assicurati che questi file siano nella root del progetto su Render:
- `render_server.py`
- `requirements.txt`
- `Procfile`

### 4. Ottieni l'URL del server

Dopo il deploy, Render ti darà un URL tipo:
```
https://your-app-name.onrender.com
```

**IMPORTANTE**: Salva questo URL, ti servirà per configurare l'ESP32!

---

## 💻 Setup MacBook

### 1. Installa dipendenze

```bash
# Installa ffmpeg (per catturare audio)
brew install ffmpeg

# Installa Python packages
pip3 install requests
```

### 2. Installa BlackHole (dispositivo audio virtuale)

BlackHole permette di catturare l'audio di sistema del MacBook.

1. Scarica da: https://github.com/ExistentialAudio/BlackHole
2. Installa il pacchetto `.pkg`
3. Configura macOS:
   - Vai su **Preferenze di Sistema** > **Suono** > **Uscita**
   - Seleziona **BlackHole 16ch** (o 2ch se preferisci)
   - Ora tutto l'audio di sistema verrà catturato da BlackHole

### 3. Configura il client MacBook

Modifica `macbook_audio_sender.py` e imposta l'URL del tuo server Render:

```python
# Alla fine del file, nella funzione main():
parser.add_argument('--render-url', 
                   default='https://your-app-name.onrender.com',  # <-- CAMBIA QUI
                   help='URL del server Render')
```

Oppure usa il parametro da linea di comando:
```bash
python3 macbook_audio_sender.py --render-url https://your-app-name.onrender.com
```

### 4. Avvia il client MacBook

```bash
python3 macbook_audio_sender.py --render-url https://your-app-name.onrender.com
```

Il client inizierà a catturare l'audio di sistema e inviarlo al server Render.

---

## 🔧 Setup ESP32

### 1. Configura l'URL del server Render

Apri `menuconfig`:
```bash
idf.py menuconfig
```

Vai a:
```
Component config
  └─> TTS Server Configuration
      └─> Render Server URL
```

Inserisci l'URL del tuo server Render (es: `https://your-app-name.onrender.com`)

Oppure modifica direttamente `sdkconfig`:
```ini
CONFIG_RENDER_SERVER_URL="https://your-app-name.onrender.com"
```

### 2. Configura WiFi

Assicurati che WiFi SSID e Password siano configurati correttamente in `menuconfig`.

### 3. Compila e flasha

```bash
# Modifica CMakeLists.txt per usare render_audio_receiver.c
# Poi compila e flasha:
idf.py build flash monitor
```

### 4. Verifica connessione

Nel monitor seriale dovresti vedere:
```
I (xxx) RENDER_AUDIO: WiFi connected! IP address: 192.168.x.x
I (xxx) RENDER_AUDIO: Stream URL: https://your-app-name.onrender.com/stream
I (xxx) RENDER_AUDIO: Starting audio stream...
I (xxx) RENDER_AUDIO: ✅ Render Audio Receiver ready!
```

---

## 🎮 Uso

### 1. Avvia il server Render
Il server Render dovrebbe essere sempre attivo (Render lo mantiene attivo automaticamente).

### 2. Avvia il client MacBook
```bash
python3 macbook_audio_sender.py --render-url https://your-app-name.onrender.com
```

### 3. L'ESP32 si connette automaticamente
L'ESP32 si connette automaticamente al server Render e inizia a ricevere lo stream audio.

### 4. Riproduci audio sul MacBook
Qualsiasi audio riprodotto sul MacBook (musica, video, chiamate) verrà:
- Catturato da BlackHole
- Inviato al server Render
- Streamato all'ESP32
- Riprodotto sull'uscita jack dell'ESP32

---

## 🔍 Troubleshooting

### L'ESP32 non riceve audio

1. **Verifica connessione WiFi**: Controlla i log seriali
2. **Verifica URL Render**: Assicurati che sia corretto in `menuconfig`
3. **Verifica server Render**: Controlla i log su Render dashboard
4. **Testa endpoint**: Apri `https://your-app-name.onrender.com/status` nel browser

### Il MacBook non invia audio

1. **Verifica BlackHole**: Assicurati che sia installato e selezionato come output audio
2. **Verifica ffmpeg**: Esegui `ffmpeg -version`
3. **Verifica connessione**: Controlla che il client si connetta al server Render

### Audio con ritardo/lag

- Il ritardo è normale (200-500ms) per streaming via internet
- Per ridurre il ritardo, usa un server più vicino geograficamente
- Considera di usare un VPS invece di Render per latenza migliore

### Server Render si spegne

- Render spegne i servizi gratuiti dopo 15 minuti di inattività
- Per mantenerlo attivo, usa un servizio di ping periodico
- Oppure passa a un piano a pagamento

---

## 📝 Note

- Il server Render gratuito ha limitazioni (si spegne dopo inattività)
- Per uso continuo, considera un VPS o piano Render a pagamento
- La qualità audio dipende dalla connessione internet di entrambi i dispositivi
- Il formato audio è MP3 a 128kbps, 44.1kHz, stereo

---

## 🔗 File Importanti

- `render_server.py` - Server Flask per Render
- `macbook_audio_sender.py` - Client per catturare e inviare audio dal MacBook
- `main/render_audio_receiver.c` - Firmware ESP32 per ricevere e riprodurre audio
- `requirements.txt` - Dipendenze Python per Render
- `Procfile` - Configurazione per Render

