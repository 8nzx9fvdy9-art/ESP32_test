╔══════════════════════════════════════════════════════════════╗
║  GUIDA RAPIDA - Comunicazione ESP32 ↔ MacBook M2           ║
╚══════════════════════════════════════════════════════════════╝

📖 LEGGI PRIMA: GUIDA_PASSO_PASSO.md
   (Guida completa passo-passo per neofiti)

🚀 QUICK START:

1. ESP32 - Configura WiFi:
   - Apri: src/main.cpp
   - Cambia: ssid e password (righe 7-8)

2. ESP32 - Compila e Flasha:
   cd /Users/edoardocolella/ESP32_test
   pio run -t upload -e esp32-audio-kit

3. ESP32 - Monitor Seriale:
   pio device monitor -b 115200 -p /dev/tty.usbserial-0001

4. MacBook - Installa dipendenze:
   pip3 install websockets

5. MacBook - Esegui client:
   python3 macbook_client.py

6. Test:
   - Digita un messaggio nel client MacBook
   - Vedi il messaggio nel monitor seriale ESP32
   - L'ESP32 invia messaggi ogni 10 secondi

⚠️ IMPORTANTE:
- Il WiFi deve essere 2.4 GHz (non 5 GHz)
- Usa il server pubblico per test (già configurato)
- Per uso reale, usa un server proprio (vedi guida)

📁 FILE IMPORTANTI:
- GUIDA_PASSO_PASSO.md → Guida completa passo-passo
- src/main.cpp → Codice ESP32 (WebSocket)
- src/main_audio_backup.cpp → Backup codice audio
- macbook_client.py → Client MacBook
- server_websocket.py → Server intermedio (opzionale)

❓ PROBLEMI?
Leggi la sezione "Problemi Comuni" in GUIDA_PASSO_PASSO.md

