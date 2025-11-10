# 🎯 ADESSA COSA FARE - Il Sistema è Pronto!

## ✅ STATO ATTUALE

Il tuo ESP32 è **CONNESSO** e il server TTS è **ATTIVO**! 🎉

- **IP ESP32:** `192.168.0.85`
- **Server HTTP:** Attivo sulla porta 80
- **WiFi:** Connesso a `2-WifiCole`
- **Server TTS:** Pronto a ricevere richieste

---

## 🚀 PROSSIMI PASSI

### Passo 1: Apri un NUOVO Terminale

**⚠️ IMPORTANTE:** 
- Lascia il terminale del monitor APERTO (quello dove vedi i log dell'ESP32)
- Apri un **NUOVO terminale** per eseguire il client Python

### Passo 2: Installa le Librerie Python

Nel nuovo terminale, esegui uno di questi comandi:

**Opzione A (Consigliata - con virtualenv):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install gtts requests
```

**Opzione B (con --user):**
```bash
pip3 install --user gtts requests
```

**Opzione C (se non funziona, usa --break-system-packages):**
```bash
pip3 install --break-system-packages gtts requests
```

### Passo 3: Vai nella Cartella del Progetto

```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
```

### Passo 4: Testa il Sistema!

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 "Ciao, questo è un test!"
```

**Se usi virtualenv (Opzione A):**
```bash
source venv/bin/activate
python3 tts_client.py --esp32-ip 192.168.0.85 "Ciao, questo è un test!"
```

---

## 🎤 COSA DOVREBBE SUCCEDERE

1. **Nel terminale Python vedrai:**
   ```
   Generando audio per: 'Ciao, questo è un test!'
   Lingua: it, TLD: com
   Audio generato: /tmp/tmpXXXXXX.mp3
   Caricando audio su server temporaneo...
   Audio caricato! URL: http://transfer.sh/...
   Inviando richiesta all'ESP32: http://192.168.0.85/play
   ✅ Testo inviato con successo!
   ```

2. **Nel monitor seriale (terminal originale) vedrai:**
   ```
   I (xxxx) TTS_SERVER: Received audio playback request
   I (xxxx) TTS_SERVER: Playing audio from URL: http://transfer.sh/...
   I (xxxx) HTTP_STREAM: HTTP stream opened
   I (xxxx) MP3_DECODER: Music info: sample_rates=24000, bits=16, ch=1
   ```

3. **Dovresti sentire la voce dalle cuffie!** 🎉

---

## 🎯 ALTRI ESEMPI

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

## 🐛 PROBLEMI COMUNI

### "No module named 'gtts'"
**Soluzione:** Installa le librerie (vedi Passo 2 sopra)

### "Connection refused"
**Soluzione:** 
- Verifica che l'IP sia corretto: `192.168.0.85`
- Assicurati che ESP32 e MacBook siano sulla stessa rete WiFi
- Controlla il monitor seriale per vedere se il server è attivo

### "Failed to upload audio"
**Soluzione:**
- Verifica che il MacBook abbia connessione Internet
- Google TTS richiede connessione Internet per generare audio

### Non sento audio
**Soluzione:**
- Controlla che le cuffie/speaker siano collegati al jack audio dell'ESP32
- Verifica che il volume non sia al minimo
- Controlla errori nel monitor seriale

---

## 📝 NOTA IMPORTANTE SULL'IP

L'IP `192.168.0.85` è quello assegnato dal router WiFi. 

**Se riavvii l'ESP32, l'IP potrebbe cambiare!**

Per vedere l'IP corrente:
1. Controlla il monitor seriale (dove hai visto "WiFi connected! IP address: ...")
2. Oppure prova a inviare un testo - se l'IP è cambiato, vedrai un errore "Connection refused"

---

## ✅ RIEPILOGO

1. ✅ ESP32 connesso al WiFi
2. ✅ Server TTS attivo
3. ⏳ Installa librerie Python (Passo 2)
4. ⏳ Testa con il comando (Passo 4)
5. 🎉 Goditi il sistema TTS!

---

## 🎊 FATTO!

Una volta che senti la voce, il sistema funziona perfettamente! Puoi ora:
- Inviare qualsiasi testo all'ESP32
- Cambiare lingua (--lang en, es, fr, ecc.)
- Usare la modalità interattiva per test multipli
- Integrare lo script in altre applicazioni

**Buon divertimento! 🚀**


