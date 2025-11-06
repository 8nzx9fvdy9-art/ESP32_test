# 🎤 Guida: Streaming Audio ESP32 -> MacBook

Questa guida spiega come far sentire i microfoni dell'ESP32 sul MacBook tramite internet.

## 📋 Requisiti

### ESP32
- ESP32-A1S v2.2 con AudioKit
- Microfoni onboard o microfono esterno via jack
- Connessione WiFi

### MacBook
- Python 3.7+
- PyAudio (richiede PortAudio su macOS)
- Connessione internet

## 🚀 Setup

### 1. Installazione PyAudio su MacBook

PyAudio richiede PortAudio. Su macOS, installalo con Homebrew:

```bash
# Installa PortAudio
brew install portaudio

# Attiva ambiente virtuale
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate

# Installa PyAudio
pip install pyaudio
```

**Nota**: Se non hai Homebrew, installalo da https://brew.sh

### 2. Carica il codice audio sull'ESP32

**Opzione A: Usa il nuovo file audio stream**

1. **Rinomina i file** (per evitare conflitti):
   ```bash
   cd /Users/edoardocolella/ESP32_test
   mv src/main.cpp src/main_websocket_backup.cpp
   mv src/main_audio_stream.cpp src/main.cpp
   ```

2. **Carica sull'ESP32**:
   - In VS Code: `Ctrl+Alt+U` (o `Cmd+Alt+U` su Mac)
   - Oppure nel terminale:
     ```bash
     pio run -t upload
     ```

3. **Apri Serial Monitor**:
   - In VS Code: `Ctrl+Alt+S` (o `Cmd+Alt+S` su Mac)
   - Oppure nel terminale:
     ```bash
     pio device monitor
     ```

**Opzione B: Modifica manualmente main.cpp**

Se preferisci mantenere entrambi i file, puoi copiare il contenuto di `main_audio_stream.cpp` in `main.cpp`.

### 3. Configurazione Microfoni

Nel file `src/main.cpp`, puoi scegliere quale microfono usare:

```cpp
// Per microfoni onboard (LINE1):
cfg.adc_input = AUDIO_HAL_ADC_INPUT_LINE1;

// Per microfono esterno via jack (LINE2):
cfg.adc_input = AUDIO_HAL_ADC_INPUT_LINE2;
```

**Nota**: Se usi il microfono esterno, assicurati che sia collegato correttamente al jack.

### 4. Avvia il Client Audio sul MacBook

```bash
# Nel Terminale Mac (non VS Code):
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_audio_client.py
```

Dovresti vedere:
- `✓ Connesso al server WebSocket!`
- `✓ Audio inizializzato (16kHz, stereo, 16-bit)`
- `In ricezione audio dall'ESP32...`

### 5. Verifica

1. **Sull'ESP32 (Serial Monitor)**:
   - Dovresti vedere: `[WebSocket] Connesso a: ...`
   - Dovresti vedere: `[Audio] Frame inviato: XXX bytes` ogni 100 frame

2. **Sul MacBook**:
   - Dovresti sentire l'audio dai microfoni dell'ESP32
   - Se non senti nulla, verifica:
     - Volume MacBook non mutato
     - ESP32 connesso al WiFi
     - Server Render attivo

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'pyaudio'"

**Soluzione**:
```bash
source venv/bin/activate
pip install pyaudio
```

### "Error: PortAudio not found" o errori di compilazione PyAudio

**Soluzione**:
```bash
# Installa PortAudio
brew install portaudio

# Reinstalla PyAudio
pip uninstall pyaudio
pip install pyaudio
```

### "Errore inizializzazione audio" sul MacBook

**Possibili cause**:
1. PortAudio non installato → `brew install portaudio`
2. Dispositivo audio non disponibile → Verifica le impostazioni audio macOS
3. Permessi macOS → Vai su Preferenze di Sistema > Privacy > Microfono

### Nessun audio ricevuto

**Verifica**:
1. ESP32 connesso al WiFi? (controlla Serial Monitor)
2. ESP32 connesso al WebSocket? (controlla Serial Monitor)
3. Client MacBook connesso? (controlla output terminale)
4. Server Render attivo? (controlla dashboard Render)
5. Volume MacBook non mutato?

### Audio distorto o con lag

**Possibili cause**:
1. Connessione internet lenta
2. Buffer audio troppo piccolo
3. Sample rate troppo alto

**Soluzioni**:
- Riduci sample rate a 8kHz (modifica `AUDIO_HAL_16K_SAMPLES` a `AUDIO_HAL_08K_SAMPLES` in `main.cpp`)
- Aumenta `AUDIO_BUFFER_SIZE` in `main.cpp` (es. 2048)
- Verifica velocità connessione WiFi

### ESP32 non si connette al WebSocket

**Verifica**:
1. WiFi connesso? (controlla Serial Monitor)
2. URL server corretto? (controlla `websocket_server` in `main.cpp`)
3. Server Render attivo? (controlla dashboard Render)

## 📊 Configurazione Audio

### Formato Audio Attuale
- **Sample Rate**: 16kHz
- **Canali**: Stereo (2)
- **Bit Depth**: 16-bit
- **Buffer Size**: 1024 bytes

### Modificare Sample Rate

Nel file `src/main.cpp`:

```cpp
// Per 8kHz (meno banda, qualità inferiore):
cfg.sample_rate = AUDIO_HAL_08K_SAMPLES;

// Per 16kHz (attuale):
cfg.sample_rate = AUDIO_HAL_16K_SAMPLES;

// Per 44.1kHz (alta qualità, più banda):
cfg.sample_rate = AUDIO_HAL_44K_SAMPLES;
```

**Nota**: Se cambi sample rate, aggiorna anche `SAMPLE_RATE` in `macbook_audio_client.py`.

### Modificare Buffer Size

Nel file `src/main.cpp`:

```cpp
// Buffer più grande = meno lag ma più memoria
const int AUDIO_BUFFER_SIZE = 2048;  // invece di 1024
```

## 🎯 Prossimi Passi

- [ ] Testare con microfoni onboard
- [ ] Testare con microfono esterno via jack
- [ ] Ottimizzare qualità/banda
- [ ] Aggiungere controllo volume
- [ ] Aggiungere indicatore livello audio

## 📝 Note

- L'audio viene trasmesso in tempo reale via WebSocket
- Il formato è PCM raw (non compresso)
- La latenza dipende dalla connessione internet
- Il server Render può aggiungere latenza (30-100ms)

## 🔄 Tornare al Codice Precedente

Se vuoi tornare al codice WebSocket testuale:

```bash
cd /Users/edoardocolella/ESP32_test
mv src/main.cpp src/main_audio_stream.cpp
mv src/main_websocket_backup.cpp src/main.cpp
```

Poi ricarica sull'ESP32.

