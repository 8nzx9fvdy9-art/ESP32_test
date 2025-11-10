# 🚀 TEST RAPIDO - Sistema TTS Funzionante!

## ✅ STATO ATTUALE

Il tuo ESP32 è **CONNESSO** e il server TTS è **ATTIVO**! 🎉

- **IP ESP32:** `192.168.0.85`
- **Server HTTP:** Attivo sulla porta 80
- **WiFi:** Connesso a `2-WifiCole`

---

## 🎯 COSA FARE ORA

### Passo 1: Apri un NUOVO Terminale

**⚠️ IMPORTANTE:** Lascia il terminale del monitor APERTO (quello dove vedi i log dell'ESP32) e apri un **NUOVO terminale**.

### Passo 2: Installa le Librerie Python

Nel nuovo terminale, esegui:

```bash
pip3 install gtts requests
```

Se hai già installato, vedrai `Requirement already satisfied`.

### Passo 3: Vai nella Cartella del Progetto

```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
```

### Passo 4: Invia Testo all'ESP32!

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 "Ciao, questo è un test!"
```

**Cosa succede:**
1. Lo script genera un file audio MP3 dal testo usando Google TTS
2. Carica il file su un server temporaneo
3. Invia l'URL all'ESP32
4. L'ESP32 scarica e riproduce l'audio
5. **Dovresti sentire la voce dalle cuffie!** 🎉

---

## 🎤 ALTRI ESEMPI

### Test in Italiano
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 "Ciao, il sistema TTS funziona perfettamente!"
```

### Test in Inglese
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --lang en "Hello, the TTS system is working!"
```

### Test in Spagnolo
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --lang es "Hola, el sistema TTS funciona!"
```

### Modalità Interattiva
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --interactive
```

Poi inserisci il testo quando richiesto. Scrivi `quit` per uscire.

---

## 🔍 COSA VEDERE

### Nel Terminale Python (nuovo terminale):
```
Generando audio per: 'Ciao, questo è un test!'
Lingua: it, TLD: com
Audio generato: /tmp/tmpXXXXXX.mp3
Caricando audio su server temporaneo...
Audio caricato! URL: http://transfer.sh/...
Inviando richiesta all'ESP32: http://192.168.0.85/play
Risposta: {"status": "ok", "message": "Audio playback started"}
✅ Testo inviato con successo!
```

### Nel Monitor Serial (terminal originale):
```
I (xxxx) TTS_SERVER: Received audio playback request
I (xxxx) TTS_SERVER: Playing audio from URL: http://transfer.sh/...
I (xxxx) TTS_SERVER: Starting audio pipeline
I (xxxx) HTTP_STREAM: HTTP stream opened
I (xxxx) MP3_DECODER: Music info: sample_rates=24000, bits=16, ch=1
I (xxxx) TTS_SERVER: Playback finished
```

---

## 🐛 PROBLEMI?

### "Connection refused"
- Verifica che l'IP sia corretto: `192.168.0.85`
- Assicurati che ESP32 e MacBook siano sulla stessa rete WiFi
- Controlla il monitor seriale per vedere se il server è attivo

### "No module named 'gtts'"
- Installa le librerie: `pip3 install gtts requests`

### Non sento audio
- Controlla che le cuffie/speaker siano collegati al jack audio dell'ESP32
- Verifica che il volume non sia al minimo
- Controlla errori nel monitor seriale

### "Failed to upload audio"
- Verifica che il MacBook abbia connessione Internet
- Google TTS richiede connessione Internet per generare audio

---

## 🎉 FATTO!

Se senti la voce, il sistema funziona perfettamente! 🎊

Puoi ora:
- Inviare qualsiasi testo all'ESP32
- Cambiare lingua (--lang en, es, fr, ecc.)
- Usare la modalità interattiva per test multipli
- Integrare lo script in altre applicazioni

---

## 📝 NOTA SULL'IP

L'IP `192.168.0.85` è quello assegnato dal router WiFi. Se riavvii l'ESP32, potrebbe cambiare. Per vedere l'IP corrente, controlla il monitor seriale o usa:

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 "Test"
```

Se l'IP cambia, aggiorna il comando con il nuovo IP.


