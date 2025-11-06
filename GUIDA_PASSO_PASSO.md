# 🚀 Guida Passo-Passo per Neofiti
## Comunicazione ESP32 ↔ MacBook M2 via WebSocket

Questa guida ti accompagnerà passo-passo per far comunicare il tuo ESP32 con il MacBook M2, anche se sono su reti WiFi diverse.

---

## 📋 Cosa ti serve

1. **ESP32-A1S AudioKit** (quello che hai già)
2. **MacBook M2** (quello che hai già)
3. **Cavo USB** per collegare ESP32 al MacBook
4. **Connessione WiFi** per entrambi i dispositivi (possono essere reti diverse!)
5. **PlatformIO** installato (dovresti averlo già)

---

## 🎯 Obiettivo

Far sì che ESP32 e MacBook possano inviarsi messaggi in tempo reale, anche se sono su WiFi diversi.

---

## 📝 PARTE 1: Configurare l'ESP32

### ⚠️ IMPORTANTE: File già configurati!

✅ **Ho già rinominato i file per te:**
- `main.cpp` (vecchio codice audio) → `main_audio_backup.cpp` (backup)
- `websocket_client.cpp` → `main.cpp` (ora è il file principale)

**Ora puoi procedere direttamente!**

### Passo 1.1: Apri il file di configurazione ESP32

1. Apri VS Code (o il tuo editor)
2. Vai nella cartella del progetto: `/Users/edoardocolella/ESP32_test`
3. Apri il file: `src/main.cpp` (ora contiene il codice WebSocket)

### Passo 1.2: Configura il WiFi dell'ESP32

Trova queste righe nel file `src/main.cpp` (circa riga 7-8):

```cpp
const char* ssid = "NOME_RETE_WIFI";
const char* password = "PASSWORD_WIFI";
```

**Sostituisci con i dati della TUA rete WiFi:**

```cpp
const char* ssid = "NomeDellaTuaRete";        // Esempio: "CasaMia"
const char* password = "PasswordDellaRete";    // Esempio: "miapassword123"
```

⚠️ **IMPORTANTE**: 
- Il WiFi deve essere **2.4 GHz** (ESP32 non supporta 5 GHz)
- Scrivi il nome esatto della rete (case-sensitive)
- Scrivi la password esatta

### Passo 1.3: Configura il server WebSocket

Trova queste righe (circa riga 16-18):

```cpp
const char* websocket_server = "echo.websocket.org";
const int websocket_port = 80;
const char* websocket_path = "/";
```

**Per ora lascia così** - useremo un server pubblico per test. Più avanti potrai cambiarlo.

### Passo 1.4: Salva il file

Salva il file (`Cmd+S` su Mac)

---

## 🔨 PARTE 2: Compilare e Flashare l'ESP32

### Passo 2.1: Collega l'ESP32 al MacBook

1. Collega l'ESP32 al MacBook con il cavo USB
2. Verifica che la porta sia `/dev/tty.usbserial-0001` (dovrebbe essere già configurata)

### Passo 2.2: Apri il Terminale

1. Apri il Terminale su MacBook (trovalo in Applicazioni > Utility)
2. Vai nella cartella del progetto:

```bash
cd /Users/edoardocolella/ESP32_test
```

### Passo 2.3: Compila e Flasha

Scrivi questo comando e premi INVIO:

```bash
pio run -t upload -e esp32-audio-kit
```

**Cosa succede:**
- PlatformIO compila il codice
- Carica il programma sull'ESP32
- Ci vogliono 1-2 minuti

**Se vedi errori:**
- Verifica che l'ESP32 sia collegato
- Verifica che la porta sia corretta in `platformio.ini`

### Passo 2.4: Apri il Monitor Seriale

In un nuovo terminale, scrivi:

```bash
cd /Users/edoardocolella/ESP32_test
pio device monitor -b 115200 -p /dev/tty.usbserial-0001
```

**Cosa vedrai:**
- L'ESP32 si connette al WiFi
- Mostra l'indirizzo IP ottenuto
- Si connette al server WebSocket
- Ogni 10 secondi invia un messaggio

**Se vedi errori:**
- "Errore: impossibile connettersi al WiFi" → Verifica SSID e password in `src/main.cpp`
- "Errore di connessione WebSocket" → Normalmente va bene, il server pubblico può essere lento

**Lascia questo terminale aperto** - vedrai i messaggi in arrivo!

---

## 💻 PARTE 3: Configurare il MacBook

### Passo 3.1: Verifica che Python sia installato

Apri il Terminale e scrivi:

```bash
python3 --version
```

**Dovresti vedere qualcosa come:** `Python 3.9.x` o superiore

**Se non è installato:**
- macOS di solito ha Python già installato
- Se non c'è, installa da: https://www.python.org/downloads/

### Passo 3.2: Installa le librerie Python necessarie

Nel Terminale, scrivi:

```bash
pip3 install websockets
```

**Cosa fa:** Installa la libreria per usare WebSocket in Python

**Se vedi errori:**
- Prova: `pip3 install --user websockets`
- Oppure: `python3 -m pip install websockets`

### Passo 3.3: Verifica che il file client esista

Controlla che esista il file `macbook_client.py` nella cartella del progetto.

---

## 🚀 PARTE 4: Eseguire il Client MacBook

### Passo 4.1: Apri un NUOVO Terminale

⚠️ **IMPORTANTE**: Lascia aperto il terminale del monitor seriale ESP32, e apri un **NUOVO** terminale per il client MacBook.

### Passo 4.2: Vai nella cartella del progetto

```bash
cd /Users/edoardocolella/ESP32_test
```

### Passo 4.3: Esegui il client Python

```bash
python3 macbook_client.py
```

**Cosa vedrai:**
- Il client si connette al server WebSocket
- Vedi un messaggio: "✓ Connesso al server WebSocket!"
- Vedi un prompt: `> `

### Passo 4.4: Invia un messaggio all'ESP32

1. Digita un messaggio, esempio: `Ciao ESP32!`
2. Premi INVIO
3. Guarda il terminale del monitor seriale ESP32 - dovresti vedere il messaggio arrivare!

### Passo 4.5: Ricevi messaggi dall'ESP32

- L'ESP32 invia automaticamente un messaggio ogni 10 secondi
- Dovresti vederlo nel terminale del client MacBook
- Formato: `[HH:MM:SS] ← Ricevuto: Messaggio da ESP32 - ...`

---

## ✅ PARTE 5: Test Completo

### Test 1: MacBook → ESP32

1. Nel terminale del client MacBook, digita: `Test 123`
2. Premi INVIO
3. Nel terminale del monitor seriale ESP32, dovresti vedere: `[WebSocket] Messaggio ricevuto: MacBook dice: Test 123`

### Test 2: ESP32 → MacBook

1. L'ESP32 invia automaticamente messaggi ogni 10 secondi
2. Nel terminale del client MacBook, dovresti vedere: `[HH:MM:SS] ← Ricevuto: Messaggio da ESP32 - ...`

### Test 3: Full-Duplex (Comunicazione Bidirezionale)

1. Invia un messaggio dal MacBook
2. L'ESP32 risponde automaticamente
3. Vedi la risposta nel client MacBook

---

## 🎉 Funziona! Cosa fare ora?

### Opzione A: Usare un Server Proprio (Più Sicuro)

Se vuoi usare un server tuo invece del server pubblico:

1. **Installa ngrok** (per esporre un server locale su internet):
   ```bash
   brew install ngrok
   ```

2. **Esegui il server locale** (in un nuovo terminale):
   ```bash
   cd /Users/edoardocolella/ESP32_test
   python3 server_websocket.py
   ```

3. **In un altro terminale, esponi con ngrok**:
   ```bash
   ngrok http 8765
   ```

4. **Copia l'URL** che ngrok ti dà (esempio: `wss://xxxx-xx-xx.ngrok-free.app`)

5. **Aggiorna ESP32 e MacBook** con questo URL:
   - In `src/main.cpp`: cambia `websocket_server` con l'URL di ngrok
   - In `macbook_client.py`: cambia `WEBSOCKET_SERVER` con l'URL di ngrok

### Opzione B: Personalizzare i Messaggi

Puoi modificare:
- **Frequenza messaggi ESP32**: In `src/main.cpp`, riga 132, cambia `10000` (10 secondi) con un altro valore
- **Messaggi personalizzati**: Modifica il testo dei messaggi nel codice

---

## ❓ Problemi Comuni

### Problema 1: ESP32 non si connette al WiFi

**Sintomi:** Vedi "Errore: impossibile connettersi al WiFi"

**Soluzioni:**
- Verifica che SSID e password siano corretti in `src/main.cpp`
- Verifica che il WiFi sia 2.4 GHz (non 5 GHz)
- Avvicina l'ESP32 al router WiFi
- Riavvia l'ESP32

### Problema 2: Client MacBook non si connette

**Sintomi:** Vedi "✗ Errore di connessione"

**Soluzioni:**
- Verifica la connessione internet del MacBook
- Il server pubblico `echo.websocket.org` a volte è lento, aspetta qualche secondo
- Prova a riavviare il client

### Problema 3: I messaggi non arrivano

**Sintomi:** Non vedi messaggi nel monitor seriale o nel client

**Soluzioni:**
- Verifica che entrambi siano connessi (vedi i messaggi di connessione)
- Il server pubblico `echo.websocket.org` è un echo server - i messaggi vengono riflessi, non inoltrati tra client
- **Per comunicazione reale tra ESP32 e MacBook, usa un server proprio** (vedi Opzione A sopra)

### Problema 4: Errore "ModuleNotFoundError: No module named 'websockets'"

**Sintomi:** Vedi questo errore quando esegui `python3 macbook_client.py`

**Soluzioni:**
```bash
pip3 install websockets
# Oppure
python3 -m pip install websockets
```

---

## 📚 Cosa hai imparato?

✅ Come configurare WiFi su ESP32  
✅ Come compilare e flashare codice ESP32  
✅ Come usare WebSocket per comunicazione in tempo reale  
✅ Come far comunicare dispositivi su reti diverse  
✅ Come usare Python per creare client WebSocket  

---

## 🎯 Prossimi Passi

1. **Personalizza i messaggi** - Modifica cosa inviano ESP32 e MacBook
2. **Aggiungi funzionalità** - Controlla LED, sensori, etc.
3. **Usa un server proprio** - Per maggiore sicurezza e controllo
4. **Aggiungi autenticazione** - Per proteggere la comunicazione

---

## 💡 Suggerimenti

- **Lascia sempre aperto il monitor seriale** per vedere cosa fa l'ESP32
- **Usa due terminali** - uno per ESP32, uno per MacBook
- **Il server pubblico è solo per test** - per uso reale usa un server proprio
- **Salva sempre i file** prima di compilare

---

## 🆘 Serve Aiuto?

Se qualcosa non funziona:
1. Controlla i messaggi di errore nel terminale
2. Verifica che tutti i passi siano stati completati
3. Rileggi la sezione "Problemi Comuni"
4. Verifica che WiFi, Python e PlatformIO siano configurati correttamente

---

**Buon divertimento! 🚀**

