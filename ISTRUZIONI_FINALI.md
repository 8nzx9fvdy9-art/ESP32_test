# 🎉 PERFETTO! Librerie Installate - Ora Testa il Sistema!

## ✅ STATO

- ✅ Librerie Python installate (`gtts`, `requests`)
- ✅ ESP32 connesso al WiFi
- ✅ Server TTS attivo
- ✅ IP ESP32: `192.168.0.85`

---

## 🚀 ORA TESTA IL SISTEMA!

### Metodo 1: Usa lo Script Helper (PIÙ SEMPLICE)

```bash
./test_tts.sh 192.168.0.85 "Ciao, questo è un test!"
```

Oppure solo:
```bash
./test_tts.sh
```

### Metodo 2: Comando Diretto (con apostrofi)

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 'Ciao, questo è un test!'
```

### Metodo 3: Modalità Interattiva (MIGLIORE per test multipli)

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --interactive
```

Poi inserisci il testo quando richiesto (senza virgolette). Scrivi `quit` per uscire.

---

## 🎤 ESEMPI

### Test in Italiano
```bash
./test_tts.sh 192.168.0.85 "Ciao, il sistema TTS funziona perfettamente!"
```

### Test in Inglese
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --lang en 'Hello, the TTS system is working!'
```

### Test in Spagnolo
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --lang es 'Hola, el sistema TTS funciona!'
```

---

## 🔍 COSA DOVREBBE SUCCEDERE

1. **Nel terminale vedrai:**
   ```
   Generando audio per: 'Ciao, questo è un test!'
   Lingua: it, TLD: com
   Audio generato: /tmp/tmpXXXXXX.mp3
   Caricando audio su server temporaneo...
   Audio caricato! URL: http://transfer.sh/...
   Inviando richiesta all'ESP32: http://192.168.0.85/play
   ✅ Testo inviato con successo!
   ```

2. **Nel monitor seriale (altro terminale) vedrai:**
   ```
   I (xxxx) TTS_SERVER: Received audio playback request
   I (xxxx) TTS_SERVER: Playing audio from URL: http://transfer.sh/...
   I (xxxx) HTTP_STREAM: HTTP stream opened
   I (xxxx) MP3_DECODER: Music info: sample_rates=24000, bits=16, ch=1
   ```

3. **Dovresti sentire la voce dalle cuffie!** 🎉

---

## 🐛 PROBLEMI?

### "Connection refused"
- Verifica che l'ESP32 sia ancora connesso (controlla il monitor seriale)
- L'IP potrebbe essere cambiato se hai riavviato l'ESP32
- Assicurati che ESP32 e MacBook siano sulla stessa rete WiFi

### "Failed to upload audio" o "No internet connection"
- Verifica che il MacBook abbia connessione Internet
- Google TTS richiede Internet per generare audio

### Non sento audio
- Controlla che le cuffie/speaker siano collegati al jack audio dell'ESP32
- Verifica che il volume non sia al minimo
- Controlla errori nel monitor seriale

### "No module named 'gtts'"
- Le librerie sono state appena installate, quindi questo non dovrebbe succedere
- Se succede, riprova: `pip3 install --break-system-packages gtts requests`

---

## ✅ PRONTO!

Ora puoi testare il sistema! Inizia con:

```bash
./test_tts.sh
```

Oppure:

```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --interactive
```

**Buon divertimento! 🎊**


