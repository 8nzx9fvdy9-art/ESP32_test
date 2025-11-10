# 🎙️ PASSO-PASSO: Caricare TTS Server su ESP32

## ✅ COMPILAZIONE COMPLETATA!

Il firmware TTS Server è stato compilato con successo! Ora devi:

---

## 📋 STEP 1: Configurare WiFi

Prima di flashare, devi configurare le credenziali WiFi.

### Opzione A: Usando menuconfig (Consigliato)

```bash
idf.py menuconfig
```

Poi:
1. Vai su **"Component config"** → Invio
2. Vai su **"TTS Server Configuration"** → Invio
3. Seleziona **"WiFi SSID"** → Invio → Scrivi il nome del tuo WiFi
4. Seleziona **"WiFi Password"** → Invio → Scrivi la password
5. Premi **ESC** più volte per uscire
6. Quando chiede di salvare, premi **S** (Sì)

### Opzione B: Modificando sdkconfig direttamente

Apri il file `sdkconfig` e cerca:
```ini
CONFIG_WIFI_SSID="myssid"
CONFIG_WIFI_PASSWORD="mypassword"
```

Cambia in:
```ini
CONFIG_WIFI_SSID="NOME_DEL_TUO_WIFI"
CONFIG_WIFI_PASSWORD="password_del_tuo_wifi"
```

**⚠️ IMPORTANTE:** Sostituisci con i tuoi dati WiFi reali!

---

## 📋 STEP 2: Flashato sull'ESP32

1. **Collega l'ESP32 al MacBook** via USB

2. **Trova la porta USB:**
   ```bash
   ls /dev/cu.usb*
   ```
   Dovresti vedere qualcosa come: `/dev/cu.usbserial-0001`

3. **Flash del firmware:**
   ```bash
   idf.py -p /dev/cu.usbserial-0001 flash monitor
   ```
   (Sostituisci `/dev/cu.usbserial-0001` con la tua porta)

---

## 📋 STEP 3: Verificare che Funzioni

Dopo il flash, nel monitor dovresti vedere:

```
I (xxxx) TTS_SERVER: Starting TTS Server...
I (xxxx) TTS_SERVER: [1] Start audio codec chip
I (xxxx) TTS_SERVER: [2] Create audio pipeline
...
I (xxxx) TTS_SERVER: [9] Start WiFi
I (xxxx) wifi: WiFi connecting to NOME_DEL_TUO_WIFI...
I (xxxx) wifi: WiFi connected!
I (xxxx) TTS_SERVER: WiFi connected! IP address: 192.168.1.100
I (xxxx) TTS_SERVER: [10] Start HTTP server
I (xxxx) TTS_SERVER: TTS Server ready! Send POST requests to http://192.168.1.100/play
```

**📝 SCRIVI L'INDIRIZZO IP!** Ti servirà dopo (es: `192.168.1.100`)

---

## 📋 STEP 4: Testare con Python Client

Apri un **nuovo terminale** e:

1. **Installa librerie Python** (se non già fatto):
   ```bash
   pip3 install gtts requests
   ```

2. **Invia testo all'ESP32:**
   ```bash
   cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
   python3 tts_client.py --esp32-ip 192.168.1.100 "Ciao, funziona!"
   ```
   (Sostituisci `192.168.1.100` con l'IP del tuo ESP32)

3. **Dovresti sentire la voce dalle cuffie!** 🎉

---

## 🐛 Problemi?

### WiFi non si connette
- Controlla SSID e password in `sdkconfig`
- Assicurati che la rete WiFi sia 2.4GHz (ESP32 non supporta 5GHz)
- Controlla il monitor seriale per errori

### "Connection refused" quando invio testo
- Verifica che ESP32 e MacBook siano sulla stessa rete WiFi
- Controlla che l'IP sia corretto
- Assicurati che il server HTTP sia avviato (vedi monitor seriale)

### Non sento audio
- Controlla che cuffie/speaker siano collegati al jack audio
- Verifica che il volume non sia al minimo
- Controlla errori nel monitor seriale

---

## ✅ FATTO!

Ora hai un sistema TTS funzionante! 

Per maggiori dettagli, vedi:
- `GUIDA_PASSO_PASSO.md` - Guida completa
- `INIZIO_RAPIDO.md` - Guida veloce
- `TTS_README.md` - Documentazione tecnica


