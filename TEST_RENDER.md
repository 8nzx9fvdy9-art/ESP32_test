# ✅ Test Connessione Render

## 🎯 Server Render Configurato

Il server WebSocket è ora disponibile su:
**https://esp32-test-q46k.onrender.com**

## 📝 File Aggiornati

✅ `src/main.cpp` - ESP32 configurato con URL Render
✅ `macbook_client.py` - Client MacBook configurato con URL Render

## 🚀 Come Testare

### Passo 1: Carica il codice sull'ESP32

1. **Apri VS Code** (o il tuo IDE)
2. **Carica il codice sull'ESP32:**
   - Premi `Ctrl+Alt+U` (o `Cmd+Alt+U` su Mac) per upload
   - Oppure usa il terminale:
     ```bash
     cd /Users/edoardocolella/ESP32_test
     pio run -t upload
     ```

3. **Apri il Serial Monitor:**
   - Premi `Ctrl+Alt+S` (o `Cmd+Alt+S` su Mac)
   - Oppure usa il terminale:
     ```bash
     pio device monitor
     ```

4. **Verifica la connessione:**
   - Dovresti vedere: `[WebSocket] Connesso a: ...`
   - Se vedi errori, controlla:
     - WiFi connesso
     - URL server corretto

### Passo 2: Avvia il Client MacBook

1. **Apri il Terminale** (Terminale Mac, non VS Code)

2. **Attiva l'ambiente virtuale:**
   ```bash
   cd /Users/edoardocolella/ESP32_test
   source venv/bin/activate
   ```

3. **Avvia il client:**
   ```bash
   python3 macbook_client.py
   ```

4. **Verifica la connessione:**
   - Dovresti vedere: `✓ Connesso al server WebSocket!`
   - Se vedi errori, controlla:
     - URL server corretto
     - Server Render attivo

### Passo 3: Testa la Comunicazione

1. **Dal MacBook:**
   - Digita un messaggio e premi INVIO
   - Esempio: `Ciao ESP32!`

2. **Sull'ESP32 (Serial Monitor):**
   - Dovresti vedere: `[WebSocket] Messaggio ricevuto: MacBook dice: Ciao ESP32!`

3. **Dall'ESP32:**
   - L'ESP32 invia automaticamente un messaggio ogni 10 secondi
   - Sul MacBook dovresti vedere: `← Ricevuto: Messaggio da ESP32 - ...`

4. **Dalla Serial Monitor:**
   - Digita un messaggio e premi INVIO
   - Sul MacBook dovresti vedere: `← Ricevuto: ESP32 dice: ...`

## 🔍 Troubleshooting

### ESP32 non si connette

**Errore**: `[WebSocket] Errore: ...`

**Soluzioni**:
1. Verifica che il WiFi sia connesso
2. Verifica che l'URL server sia corretto: `esp32-test-q46k.onrender.com`
3. Verifica che il server Render sia attivo (vai su https://esp32-test-q46k.onrender.com)
4. Controlla che la porta sia 443 (HTTPS/WSS)

### MacBook non si connette

**Errore**: `✗ Errore di connessione: ...`

**Soluzioni**:
1. Verifica che l'URL server sia corretto: `esp32-test-q46k.onrender.com`
2. Verifica che il server Render sia attivo
3. Controlla che usi `wss://` (non `ws://`)
4. Verifica che l'ambiente virtuale sia attivo: `source venv/bin/activate`

### Server Render non risponde

**Errore**: `HTTP 404` o `Connection refused`

**Soluzioni**:
1. Vai su https://dashboard.render.com
2. Verifica che il servizio sia "Live" (non "Sleeping")
3. Se è "Sleeping", Render lo sveglierà automaticamente alla prima richiesta (può richiedere 30-60 secondi)
4. Controlla i log su Render per errori

### Messaggi non arrivano

**Problema**: Connessione OK ma messaggi non arrivano

**Soluzioni**:
1. Verifica che entrambi (ESP32 e MacBook) siano connessi
2. Il server richiede almeno 2 client connessi per inoltrare messaggi
3. Controlla i log del server Render per vedere i messaggi in arrivo

## 📊 Verifica Server Render

Per verificare che il server sia attivo:

1. **Vai su Render Dashboard:**
   - https://dashboard.render.com
   - Clicca sul tuo servizio "esp32-test"

2. **Controlla lo stato:**
   - Dovrebbe essere "Live" (verde)
   - Se è "Sleeping" (grigio), Render lo sveglierà alla prima richiesta

3. **Controlla i log:**
   - Clicca su "Logs"
   - Dovresti vedere: `Server in ascolto su ws://0.0.0.0:XXXX`
   - Quando un client si connette: `Nuovo client connesso. Totale: X`

## 🎉 Successo!

Se tutto funziona:
- ✅ ESP32 connesso al server Render
- ✅ MacBook connesso al server Render
- ✅ Messaggi inviati da ESP32 arrivano al MacBook
- ✅ Messaggi inviati da MacBook arrivano all'ESP32

**Comunicazione full-duplex funzionante! 🚀**

