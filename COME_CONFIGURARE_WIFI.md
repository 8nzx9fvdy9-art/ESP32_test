# 📶 Come Configurare WiFi per ESP32 TTS Server

## 🎯 METODO 1: Usando menuconfig (CONSIGLIATO - Più facile)

### Passo 1: Apri menuconfig

```bash
cd /Users/edoardocolella/esp/esp-adf/examples/get-started/play_mp3_control
idf.py menuconfig
```

### Passo 2: Naviga nel menu

1. Vedrai un menu a schermo intero
2. Usa le **frecce SU/GIÙ** per muoverti
3. Usa **Invio** per entrare in una voce
4. Usa **ESC** per tornare indietro

### Passo 3: Vai alla configurazione WiFi

Segui questo percorso:
```
Component config  [Invio]
  └─> TTS Server Configuration  [Invio]
      ├─> WiFi SSID  [Invio]
      └─> WiFi Password  [Invio]
```

### Passo 4: Inserisci i dati WiFi

**Per WiFi SSID:**
1. Seleziona `WiFi SSID` e premi Invio
2. Cancella il testo esistente (es: "myssid")
3. Scrivi il nome della tua rete WiFi (es: "CasaMia" o "TP-Link_123")
4. Premi Invio per confermare

**Per WiFi Password:**
1. Seleziona `WiFi Password` e premi Invio
2. Cancella il testo esistente (es: "mypassword")
3. Scrivi la password del tuo WiFi
4. Premi Invio per confermare

### Passo 5: Salva ed Esci

1. Premi **ESC** più volte fino a tornare al menu principale
2. Quando chiede "Save?", premi **S** (Sì)
3. Premi **Q** per uscire

---

## 🎯 METODO 2: Modificando direttamente sdkconfig (PIÙ VELOCE)

### Passo 1: Apri il file sdkconfig

Apri il file `sdkconfig` nella cartella del progetto con un editor di testo qualsiasi (TextEdit, VS Code, nano, ecc.)

### Passo 2: Trova le righe WiFi

Cerca queste righe (premi Cmd+F e cerca "WIFI_SSID"):

```ini
CONFIG_WIFI_SSID="myssid"
CONFIG_WIFI_PASSWORD="mypassword"
```

### Passo 3: Modifica i valori

Sostituisci con i tuoi dati WiFi:

```ini
CONFIG_WIFI_SSID="NOME_DEL_TUO_WIFI"
CONFIG_WIFI_PASSWORD="password_del_tuo_wifi"
```

**ESEMPIO:**
```ini
CONFIG_WIFI_SSID="CasaMia"
CONFIG_WIFI_PASSWORD="miaPassword123"
```

### Passo 4: Salva il file

Salva il file (Cmd+S)

---

## ✅ Verifica che sia Configurato

Esegui questo comando per verificare:

```bash
grep -i "WIFI_SSID\|WIFI_PASSWORD" sdkconfig
```

Dovresti vedere:
```
CONFIG_WIFI_SSID="NOME_DEL_TUO_WIFI"
CONFIG_WIFI_PASSWORD="password_del_tuo_wifi"
```

---

## ⚠️ IMPORTANTE

1. **Il nome WiFi (SSID) deve essere ESATTO** - controlla maiuscole/minuscole
2. **La password deve essere CORRETTA** - controlla di non avere errori di battitura
3. **Il WiFi deve essere 2.4GHz** - ESP32 non supporta reti WiFi 5GHz
4. **MacBook e ESP32 devono essere sulla stessa rete WiFi**

---

## 🚀 Dopo aver Configurato WiFi

1. **Compila il progetto:**
   ```bash
   idf.py build
   ```

2. **Flash sull'ESP32:**
   ```bash
   idf.py -p /dev/cu.usbserial-0001 flash monitor
   ```

3. **Nel monitor vedrai:**
   ```
   I (xxxx) wifi: WiFi connecting to NOME_DEL_TUO_WIFI...
   I (xxxx) wifi: WiFi connected!
   I (xxxx) TTS_SERVER: WiFi connected! IP address: 192.168.1.100
   ```

---

## 🐛 Problemi?

### "WiFi connection failed"
- Controlla che SSID e password siano corretti
- Verifica che la rete WiFi sia 2.4GHz
- Controlla che non ci siano caratteri speciali strani nella password

### "Invalid SSID or password"
- Ricontrolla il nome del WiFi (SSID)
- Verifica che la password sia corretta
- Assicurati che non ci siano spazi extra all'inizio o alla fine

---

## 📝 Nota

I dati WiFi vengono salvati nel file `sdkconfig`. Questo file è già nel `.gitignore`, quindi non verrà committato su Git (sicurezza).


