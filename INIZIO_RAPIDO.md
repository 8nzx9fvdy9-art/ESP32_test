# 🚀 INIZIO RAPIDO - Sistema TTS ESP32

## ⚡ Guida Veloce (5 minuti)

### 1️⃣ Attiva Modalità TTS Server

```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
./switch_to_tts.sh
```

### 2️⃣ Configura WiFi

```bash
./setup_wifi.sh
```

Ti chiederà SSID e password del WiFi.

### 3️⃣ Attiva Ambiente ESP-IDF

```bash
. $HOME/esp/v5.1.6/esp-idf/export.sh
```

### 4️⃣ Compila e Flasha

```bash
idf.py build
idf.py -p /dev/cu.usbserial-0001 flash monitor
```

(Sostituisci `/dev/cu.usbserial-0001` con la tua porta USB)

### 5️⃣ Annota l'IP

Nel monitor, cerca:
```
WiFi connected! IP address: 192.168.1.100
```

**Scrivi questo IP!** (es: `192.168.1.100`)

### 6️⃣ Installa Python Libraries

Apri un **nuovo terminale**:

```bash
pip3 install gtts requests
```

### 7️⃣ Invia Testo!

```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
python3 tts_client.py --esp32-ip 192.168.1.100 "Ciao, funziona!"
```

(Sostituisci `192.168.1.100` con l'IP del tuo ESP32)

### 🎉 Dovresti sentire la voce!

---

## 📖 Per maggiori dettagli

Vedi `GUIDA_PASSO_PASSO.md` per una guida completa e dettagliata.

---

## 🔄 Tornare alla Modalità SD Card

Se vuoi tornare a riprodurre file dalla SD card:

```bash
./switch_to_sdcard.sh
idf.py build
idf.py -p /dev/cu.usbserial-0001 flash
```


