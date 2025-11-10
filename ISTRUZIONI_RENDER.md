# 🎵 Istruzioni Rapide - Streaming Audio via Render

## ✅ Server Render Configurato

Il tuo server Render è già configurato:
- **URL**: `https://esp32-test-q46k.onrender.com`

---

## 🚀 Setup Rapido (3 passi)

### 1️⃣ Configura ESP32

```bash
# Esegui lo script di configurazione
./configure_render.sh
```

Oppure manualmente:
```bash
idf.py menuconfig
# Vai a: Component config > TTS Server Configuration
# - Imposta Render Server URL: https://esp32-test-q46k.onrender.com
# - Imposta WiFi SSID e Password
```

### 2️⃣ Compila e Flasha ESP32

```bash
idf.py build flash monitor
```

Nel monitor seriale dovresti vedere:
```
I (xxx) RENDER_AUDIO: Stream URL: https://esp32-test-q46k.onrender.com/stream
I (xxx) RENDER_AUDIO: ✅ Render Audio Receiver ready!
```

### 3️⃣ Avvia Client MacBook

```bash
# Usa lo script helper
./start_macbook_sender.sh
```

Oppure manualmente:
```bash
python3 macbook_audio_sender.py --render-url https://esp32-test-q46k.onrender.com
```

---

## ✅ Verifica Funzionamento

### Test Server Render

Apri nel browser:
- Status: https://esp32-test-q46k.onrender.com/status
- Dovresti vedere: `{"status": "online", ...}`

### Test Client MacBook

1. Avvia il client MacBook
2. Riproduci audio sul MacBook (musica, video, ecc.)
3. Dovresti vedere nel terminale:
   ```
   ✅ Cattura audio avviata
   Invio audio a https://esp32-test-q46k.onrender.com/audio
   ```

### Test ESP32

1. Verifica log seriale:
   ```
   I (xxx) RENDER_AUDIO: Music info: sample_rates=44100, bits=16, ch=2
   I (xxx) RENDER_AUDIO: I2S clock configured: 44100 Hz, 16 bit, 2 channels
   ```
2. Collega cuffie al jack dell'ESP32
3. Dovresti sentire l'audio del MacBook!

---

## 🔧 Troubleshooting

### ESP32 non si connette

1. **Verifica WiFi**:
   ```bash
   idf.py menuconfig
   # Verifica WiFi SSID e Password
   ```

2. **Verifica URL Render**:
   ```bash
   grep CONFIG_RENDER_SERVER_URL sdkconfig
   # Dovrebbe essere: CONFIG_RENDER_SERVER_URL="https://esp32-test-q46k.onrender.com"
   ```

3. **Controlla log seriale**:
   - Cerca errori di connessione
   - Verifica che WiFi sia connesso

### MacBook non invia audio

1. **Verifica BlackHole**:
   - Preferenze di Sistema > Suono > Uscita
   - Deve essere selezionato **BlackHole 16ch** (o 2ch)

2. **Verifica ffmpeg**:
   ```bash
   ffmpeg -version
   ```

3. **Verifica connessione server**:
   ```bash
   curl https://esp32-test-q46k.onrender.com/status
   ```

### Nessun audio sull'ESP32

1. **Verifica volume**:
   - Controlla log seriale per messaggi di volume
   - Volume di default: 70%

2. **Verifica cuffie**:
   - Collegate al jack 3.5mm
   - Volume cuffie non al minimo

3. **Verifica stream**:
   - Controlla che il client MacBook stia inviando audio
   - Verifica status server: https://esp32-test-q46k.onrender.com/status

---

## 📝 Note Importanti

- ⚠️ **Server Render gratuito**: Si spegne dopo 15 minuti di inattività
- ⏱️ **Ritardo audio**: Normale (200-500ms) per streaming via internet
- 🔊 **Qualità audio**: MP3 128kbps, 44.1kHz, stereo
- 🔌 **BlackHole**: Necessario per catturare audio di sistema su macOS

---

## 🎮 Uso Quotidiano

### Avvio Rapido

1. **Avvia client MacBook**:
   ```bash
   ./start_macbook_sender.sh
   ```

2. **L'ESP32 si connette automaticamente** quando è acceso

3. **Riproduci audio sul MacBook** e ascolta sull'ESP32!

### Stop

- Premi **Ctrl+C** nel terminale del client MacBook per fermare

---

## 🔗 Link Utili

- Server Render: https://esp32-test-q46k.onrender.com
- Status Server: https://esp32-test-q46k.onrender.com/status
- BlackHole: https://github.com/ExistentialAudio/BlackHole

