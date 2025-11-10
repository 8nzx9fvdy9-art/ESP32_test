# 🔇 Risoluzione Problema Audio

## Problema: Non si sente audio

## ✅ SOLUZIONI APPLICATE

Ho aggiunto al codice:
1. **Impostazione volume** (70% di default)
2. **Unmute automatico** del codec
3. **Verifica volume** dopo l'impostazione
4. **Delay** prima di avviare la pipeline

## 🔧 VERIFICHE DA FARE

### 1. Ricompila e Flasha

```bash
idf.py build flash monitor
```

### 2. Controlla i Log

Nel monitor seriale dovresti vedere:
```
I (xxx) TTS_SERVER: [1.1] Setting volume to 70%
I (xxx) TTS_SERVER: [1.2] Volume set to 70%
I (xxx) TTS_SERVER: [1.3] Audio unmuted
```

### 3. Verifica Hardware

- ✅ **Cuffie/Speaker collegati** al jack audio 3.5mm dell'ESP32-A1S
- ✅ **Volume cuffie** non al minimo
- ✅ **Jack inserito completamente** nel connettore
- ✅ **Cuffie funzionanti** (prova con un altro dispositivo)

### 4. Test Audio

Dopo il flash, invia testo:
```bash
python3 tts_client.py --esp32-ip 192.168.0.85 --interactive
```

### 5. Controlla nel Monitor

Dovresti vedere:
```
I (xxx) TTS_SERVER: Playing audio from URL: http://192.168.0.98:8080/...
I (xxx) MP3_DECODER: MP3 opened
I (xxx) TTS_SERVER: Music info: sample_rates=24000, bits=16, ch=1
I (xxx) TTS_SERVER: I2S clock configured: 24000 Hz, 16 bit, 1 channels
```

## 🐛 SE ANCORA NON FUNZIONA

### Opzione 1: Aumenta il Volume

Modifica in `tts_server_example.c` linea ~306:
```c
int volume = 90;  // Aumenta da 70 a 90
```

### Opzione 2: Verifica Codec

Controlla nel monitor se ci sono errori del codec:
```
E (xxx) AUDIO_HAL: ...
```

### Opzione 3: Test Hardware

1. Prova le cuffie con un altro dispositivo
2. Prova un altro paio di cuffie
3. Verifica che il jack sia inserito correttamente

### Opzione 4: Verifica I2S Pins

I pin I2S sono configurati in `board_pins_config.c`:
- WS (Word Select): GPIO2
- BCK (Bit Clock): GPIO4
- DATA: GPIO16
- MCK (Master Clock): GPIO0

## 📝 NOTA

Se il volume è impostato ma non senti nulla, potrebbe essere:
1. Problema hardware (codec, I2S, jack)
2. Problema di configurazione I2S
3. Problema con le cuffie

Controlla i log nel monitor per vedere se ci sono errori.


