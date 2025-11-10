# 📝 RIEPILOGO SEMPLICE - Sistema TTS ESP32

## 🎯 Cosa abbiamo fatto

Abbiamo creato un sistema che:
1. Riceve testo dal tuo MacBook
2. Genera audio con Google TTS
3. Lo invia all'ESP32 via WiFi
4. L'ESP32 riproduce l'audio tramite cuffie/speaker

---

## 📋 FILE CREATI

### File Principali:
- `main/tts_server_example.c` - Codice server HTTP sull'ESP32
- `tts_client.py` - Script Python per inviare testo
- `GUIDA_PASSO_PASSO.md` - Guida completa dettagliata
- `INIZIO_RAPIDO.md` - Guida veloce
- `TTS_README.md` - Documentazione tecnica

### Script Helper:
- `switch_to_tts.sh` - Passa alla modalità TTS Server
- `switch_to_sdcard.sh` - Torna alla modalità SD Card
- `setup_wifi.sh` - Aiuta a configurare WiFi

---

## 🚀 PROCEDURA RAPIDA

### Passo 1: Passa alla Modalità TTS
```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
./switch_to_tts.sh
```

### Passo 2: Configura WiFi
```bash
idf.py menuconfig
```
Vai su: `Component config → TTS Server Configuration`
Imposta SSID e Password del WiFi

### Passo 3: Compila e Flasha
```bash
. $HOME/esp/v5.1.6/esp-idf/export.sh
idf.py build
idf.py -p /dev/cu.usbserial-0001 flash monitor
```

### Passo 4: Annota l'IP
Nel monitor, cerca: `WiFi connected! IP address: 192.168.1.100`
**Scrivi questo numero!**

### Passo 5: Installa Python Libraries
Apri un nuovo terminale:
```bash
pip3 install gtts requests
```

### Passo 6: Invia Testo!
```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
python3 tts_client.py --esp32-ip 192.168.1.100 "Ciao!"
```

---

## 📚 DOCUMENTAZIONE

- **Principiante?** → Leggi `GUIDA_PASSO_PASSO.md`
- **Vuoi andare veloce?** → Leggi `INIZIO_RAPIDO.md`
- **Dettagli tecnici?** → Leggi `TTS_README.md`

---

## 🔧 COMANDI UTILI

### Cambiare Modalità:
```bash
./switch_to_tts.sh      # Attiva TTS Server
./switch_to_sdcard.sh   # Torna a SD Card
```

### Compilare e Flashare:
```bash
idf.py build
idf.py -p PORTA flash monitor
```

### Inviare Testo:
```bash
python3 tts_client.py "Testo da pronunciare"
python3 tts_client.py --interactive  # Modalità interattiva
```

---

## ❓ DOMANDE FREQUENTI

**Q: Come trovo la porta USB dell'ESP32?**
A: Esegui `ls /dev/cu.usb*` nel terminale

**Q: Come trovo l'IP dell'ESP32?**
A: Guarda il monitor seriale dopo il flash, cerca "WiFi connected! IP address:"

**Q: Non sento audio, cosa fare?**
A: 
1. Controlla che cuffie/speaker siano collegati
2. Verifica che il volume non sia al minimo
3. Controlla errori nel monitor seriale

**Q: Come cambio lingua?**
A: Usa `--lang`:
```bash
python3 tts_client.py --lang en "Hello"
python3 tts_client.py --lang es "Hola"
```

---

## 🎓 PROSSIMI PASSI

1. ✅ Sistema base funzionante
2. 🎨 Crea interfaccia web per inviare testo
3. 🌐 Integra con servizi cloud
4. 🔊 Aggiungi controllo volume via web
5. 📱 Crea app mobile per controllare l'ESP32

---

**Buon divertimento! 🎉**


