#include <Arduino.h>
#include <SD_MMC.h>
#include <FS.h>
#include "AudioKitHAL.h"
#include "AudioFileSourceFS.h"
#include "AudioFileSourceBuffer.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"
#include <WiFi.h>
#include <esp_bt.h>
#include <driver/i2s.h>

static const char* kAudioFilePath = "/test.mp3"; // file sulla microSD

using namespace audiokit;
AudioKit kit;                          // Inizializza ES8388
AudioFileSourceFS *file = nullptr;     // Sorgente da FS (SD_MMC)
AudioFileSourceBuffer *fileBuf = nullptr; // Bufferizzazione per evitare singhiozzi
AudioGeneratorMP3 *mp3 = nullptr;      // Decoder MP3
AudioOutputI2S *out = nullptr;         // Uscita I2S verso ES8388

// Pin SDMMC tipici su ESP32-AudioKit A1S
static const int PIN_SD_CLK = 14;
static const int PIN_SD_CMD = 15;
static const int PIN_SD_D0  = 2;
static const int PIN_SD_D1  = 4;
static const int PIN_SD_D2  = 12;
static const int PIN_SD_D3  = 13;

static bool mountSDWithRetries() {
	// forziamo i pin e pull-up interni (CMD/D0..D3) per aiutare durante init
	SD_MMC.setPins(PIN_SD_CLK, PIN_SD_CMD, PIN_SD_D0, PIN_SD_D1, PIN_SD_D2, PIN_SD_D3);
	pinMode(PIN_SD_CMD, INPUT_PULLUP);
	pinMode(PIN_SD_D0,  INPUT_PULLUP);
	pinMode(PIN_SD_D1,  INPUT_PULLUP);
	pinMode(PIN_SD_D2,  INPUT_PULLUP);
	pinMode(PIN_SD_D3,  INPUT_PULLUP);

	struct TryCfg { bool oneBit; uint32_t freqKHz; } tries[] = {
		{true,   4000},  // 1-bit 4 MHz (più stabile - priorità)
		{true,   2000},  // 1-bit 2 MHz (ancora più lento ma stabile)
		{false,  4000},  // 4-bit 4 MHz
		{true,  10000},  // 1-bit 10 MHz (ultimo tentativo)
		{false, 10000}   // 4-bit 10 MHz (ultimo tentativo)
	};
	for (auto &t : tries) {
		Serial.print("SD_MMC.begin  ");
		Serial.print(t.oneBit ? "1-bit" : "4-bit");
		Serial.print(", ");
		Serial.print(t.freqKHz);
		Serial.println(" kHz");
		if (SD_MMC.begin("/sdcard", t.oneBit, true, t.freqKHz)) {
			return true;
		}
		// breve pausa tra i tentativi
		delay(100);
	}
	return false;
}

// Legge il titolo ID3v1 (ultimi 128 byte) dal file MP3; ritorna stringa vuota se non presente
static String readID3v1Title(fs::FS &fs, const char* path) {
	File f = fs.open(path, "r");
	if (!f) return String("");
	uint64_t sz = f.size();
	if (sz < 128) { f.close(); return String(""); }
	if (!f.seek(sz - 128)) { f.close(); return String(""); }
	uint8_t buf[128];
	int n = f.read(buf, sizeof(buf));
	f.close();
	if (n != 128) return String("");
	if (!(buf[0]=='T' && buf[1]=='A' && buf[2]=='G')) return String("");
	char title[31];
	memcpy(title, &buf[3], 30);
	title[30] = '\0';
	String s = String(title);
	s.trim();
	return s;
}

void setup() {
	Serial.begin(115200);
	while (!Serial) { ; }
	Serial.println();
	Serial.println("ESP32-A1S: MP3 da SD con ESP8266Audio");

	// Riduci interferenze: disabilita WiFi/BLE e usa massima frequenza CPU
	WiFi.mode(WIFI_OFF);
	btStop();
	setCpuFrequencyMhz(240);

	// Inizializza AudioKitHAL per ES8388 (volume e codec)
	AudioKitConfig cfg = kit.defaultConfig();
	cfg.sample_rate = AUDIO_HAL_44K_SAMPLES;
	if (!kit.begin(cfg)) {
		Serial.println("[ERRORE] ES8388 init fallito");
		for(;;) delay(1000);
	}
	kit.setVolume(80); // Volume 0..100
	delay(100); // Stabilizza ES8388
	
	// Ferma I2S_NUM_0 inizializzato da AudioKitHAL per evitare conflitti con AudioOutputI2S
	// AudioOutputI2S lo inizializzerà di nuovo con la sua configurazione
	i2s_driver_uninstall(I2S_NUM_0);
	delay(50);

	if (!mountSDWithRetries()) {
		Serial.println("[ERRORE] SD_MMC.begin fallito (FAT32?)");
		for (;;) delay(1000);
	}
	// Info SD
	uint8_t ctype = SD_MMC.cardType();
	uint64_t csize = SD_MMC.cardSize();
	Serial.print("SD tipo: "); Serial.println(ctype == CARD_NONE ? "Nessuna" : (ctype==CARD_MMC?"MMC":ctype==CARD_SD?"SDSC":ctype==CARD_SDHC?"SDHC/SDXC":"Sconosciuta"));
	Serial.print("SD capacita: "); Serial.print((double)csize / (1024.0*1024.0*1024.0), 2); Serial.println(" GB");
	Serial.println("Contenuto root:");
	{
		File root = SD_MMC.open("/");
		for (int i=0; i<10 && root; ++i) {
			File f = root.openNextFile();
			if (!f) break;
			Serial.print(f.isDirectory()?"[DIR] ":"      ");
			Serial.print(f.name());
			if (!f.isDirectory()) { Serial.print("  "); Serial.print((uint32_t)f.size()); Serial.print(" bytes"); }
			Serial.println("");
			f.close();
		}
	}

	file = new AudioFileSourceFS(SD_MMC, kAudioFilePath);
	if (!file || !file->isOpen()) {
		Serial.print("[ERRORE] Apertura file: "); Serial.println(kAudioFilePath);
		for (;;) delay(1000);
	}
	// Leggi e mostra il titolo ID3v1 se presente
	{
		String title = readID3v1Title(SD_MMC, kAudioFilePath);
		if (title.length()) {
			Serial.print("Titolo (ID3v1): "); Serial.println(title);
		} else {
			Serial.println("Titolo ID3v1 non trovato (o tag assente)");
		}
	}

	Serial.println("Configuro I2S: BCLK=27 LRCK=25 DOUT=26");
	out = new AudioOutputI2S();
	out->SetPinout(27, 25, 26);
	out->SetChannels(2);
	out->SetRate(44100); // 44.1 kHz è più stabile per MP3
	out->SetBitsPerSample(16);
	out->SetOutputModeMono(false);
	out->SetGain(1.0f);

	// Buffer ottimizzato (48KB) per lettura fluida senza singhiozzi
	// Ridotto da 96KB a 48KB per problemi di memoria DRAM
	static uint8_t s_mp3Buf[48 * 1024];
	fileBuf = new AudioFileSourceBuffer(file, s_mp3Buf, sizeof(s_mp3Buf));

	mp3 = new AudioGeneratorMP3();
	// Delay per stabilizzare tutto prima di iniziare
	delay(100);
	if (!mp3->begin(fileBuf, out)) {
		Serial.println("[ERRORE] I2S/mp3 begin fallito");
		for(;;) delay(1000);
	}
	Serial.print("Riproduzione: "); Serial.println(kAudioFilePath);
	// Aspetta un po' che il buffer si riempia
	delay(200);
}

void loop() {
	if (mp3) {
		if (!mp3->isRunning()) {
			Serial.println("Brano terminato");
			mp3->stop();
			for(;;) delay(1000);
		}
		// Esegui loop più volte per evitare buffer underrun
		for (int i = 0; i < 3; i++) {
			if (!mp3->loop()) {
				// Se fallisce, potrebbe essere fine del brano o errore
				break;
			}
		}
		// Piccola pausa per evitare saturare la CPU
		delay(1);
	}
}
