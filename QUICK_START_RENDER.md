# 🚀 Quick Start - Streaming Audio via Render

## Setup Rapido (5 minuti)

### 1️⃣ Deploy Server Render (2 min)

1. Vai su [render.com](https://render.com) e crea account
2. Crea nuovo "Web Service"
3. Collega repository o carica manualmente:
   - `render_server.py`
   - `requirements.txt`
   - `Procfile`
4. Deploy e copia l'URL (es: `https://your-app.onrender.com`)

### 2️⃣ Configura MacBook (1 min)

```bash
# Installa BlackHole (dispositivo audio virtuale)
# Scarica da: https://github.com/ExistentialAudio/BlackHole

# Installa ffmpeg
brew install ffmpeg

# Installa dipendenze Python
pip3 install requests
```

**Configura macOS:**
- Preferenze di Sistema > Suono > Uscita
- Seleziona **BlackHole 16ch**

### 3️⃣ Configura ESP32 (1 min)

```bash
# Apri menuconfig
idf.py menuconfig

# Vai a: Component config > TTS Server Configuration
# - Imposta WiFi SSID e Password
# - Imposta Render Server URL (es: https://your-app.onrender.com)

# Compila e flasha
idf.py build flash monitor
```

### 4️⃣ Avvia tutto (1 min)

**Terminale 1 - MacBook:**
```bash
python3 macbook_audio_sender.py --render-url https://your-app.onrender.com
```

**Terminale 2 - Monitor ESP32:**
```bash
idf.py monitor
```

### ✅ Fatto!

Ora qualsiasi audio sul MacBook verrà trasmesso all'ESP32 e riprodotto sul jack!

---

## 🔧 Troubleshooting Rapido

**ESP32 non si connette?**
- Verifica WiFi in `menuconfig`
- Verifica URL Render in `menuconfig`
- Controlla log seriale

**MacBook non invia audio?**
- Verifica che BlackHole sia selezionato come output audio
- Verifica che ffmpeg sia installato: `ffmpeg -version`
- Controlla che il server Render sia online: `https://your-app.onrender.com/status`

**Nessun audio sull'ESP32?**
- Verifica volume in log seriale
- Verifica che cuffie siano collegate al jack
- Controlla che lo stream sia attivo: `https://your-app.onrender.com/status`

---

## 📝 Note Importanti

- Il server Render gratuito si spegne dopo 15 min di inattività
- Per uso continuo, considera un piano a pagamento o VPS
- Il ritardo audio è normale (200-500ms) per streaming via internet

