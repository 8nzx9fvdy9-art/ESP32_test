# ESP32-A1S AudioKit - Riproduzione MP3 da microSD

Questo progetto PlatformIO per ESP32-AudioKit (ESP32-A1S con codec ES8388) riproduce un file MP3 presente sulla microSD nelle cuffie (jack da 3.5mm sull'AudioKit).

## Requisiti

- PlatformIO (VS Code o CLI)
- Board: ESP32-AudioKit (A1S, ES8388)
- microSD formattata FAT32, con un file MP3 (es. `test.mp3`) nella root

Le librerie necessarie sono dichiarate in `platformio.ini` e verranno installate automaticamente:
- `AudioTools`
- `ESP32-Audio-Kit`

## File importante da preparare sulla microSD

- Copia un file MP3 nella root della SD e chiamalo `test.mp3` (o cambia il percorso in `src/main.cpp`, variabile `kAudioFilePath`).

## Pin e slot SD

L'ESP32-AudioKit usa lo slot SDMMC onboard (non SPI). Il codice monta la SD su `/sdcard` in modalità 1-bit per massimizzare la compatibilità.

## Build & Flash

1. Collega l'ESP32-AudioKit al PC via USB.
2. Apri questa cartella con VS Code + PlatformIO.
3. Seleziona l'ambiente `esp32-audio-kit` e compila/flasha.
4. Apri il monitor seriale a 115200 baud.

Dovresti vedere messaggi di inizializzazione e l'avvio della riproduzione del file indicato.

## Volume

Il volume di uscita è impostato al 80% nel setup. Puoi modificarlo nella configurazione `cfg.volume` in `src/main.cpp`.

## Cambio brano

Modifica la costante `kAudioFilePath` in `src/main.cpp`, ad esempio:

```
static const char* kAudioFilePath = "/miei_brani/canzone.mp3";
```

## Note

- Se la SD non viene montata, riprova con un'altra scheda e assicurati sia FAT32.
- Assicurati che il file sia MP3 (il decoder usato è MP3 Helix). Per WAV/FLAC basterà sostituire il decoder nel codice.







