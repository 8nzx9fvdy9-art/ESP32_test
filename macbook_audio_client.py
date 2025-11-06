#!/usr/bin/env python3
"""
Client WebSocket per MacBook M2 - Ricezione e riproduzione audio
Riceve audio dall'ESP32 tramite server WebSocket e lo riproduce
"""

import asyncio
import websockets
import json
import sys
import threading
import queue
from datetime import datetime
import pyaudio

# ===== CONFIGURAZIONE SERVER =====
WEBSOCKET_SERVER = "esp32-test-q46k.onrender.com"
WEBSOCKET_PORT = 443
WEBSOCKET_PATH = "/"
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}{WEBSOCKET_PATH}"

# ===== CONFIGURAZIONE AUDIO =====
# Formato audio dall'ESP32: 16-bit stereo, 16kHz
SAMPLE_RATE = 16000
CHANNELS = 2  # Stereo
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
CHUNK_SIZE = 1024  # Dimensione buffer audio

class MacBookAudioClient:
    def __init__(self):
        self.websocket = None
        self.connected = False
        self.audio_queue = queue.Queue(maxsize=10)  # Buffer audio
        self.audio_stream = None
        self.pyaudio_instance = None
        
    async def connect(self):
        """Connette al server WebSocket"""
        try:
            print(f"Connessione a {WEBSOCKET_URL}...")
            self.websocket = await websockets.connect(
                WEBSOCKET_URL,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10
            )
            self.connected = True
            print("✓ Connesso al server WebSocket!")
            return True
        except Exception as e:
            print(f"✗ Errore di connessione: {e}")
            return False
    
    def init_audio(self):
        """Inizializza PyAudio per riproduzione"""
        try:
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Apri stream audio per output
            self.audio_stream = self.pyaudio_instance.open(
                format=self.pyaudio_instance.get_format_from_width(SAMPLE_WIDTH),
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                output=True,
                frames_per_buffer=CHUNK_SIZE
            )
            print("✓ Audio inizializzato (16kHz, stereo, 16-bit)")
            return True
        except Exception as e:
            print(f"✗ Errore inizializzazione audio: {e}")
            print("Assicurati di aver installato pyaudio: pip install pyaudio")
            return False
    
    def play_audio(self):
        """Riproduce audio dalla coda in un thread separato"""
        while self.connected or not self.audio_queue.empty():
            try:
                # Preleva audio dalla coda (timeout 0.1 secondi)
                audio_data = self.audio_queue.get(timeout=0.1)
                
                if self.audio_stream and not self.audio_stream.is_stopped():
                    self.audio_stream.write(audio_data)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Errore nella riproduzione audio: {e}")
                break
    
    async def receive_audio(self):
        """Riceve audio dall'ESP32 tramite server"""
        if not self.connected or not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                if isinstance(message, bytes):
                    # Dati binari (audio)
                    try:
                        # Aggiungi audio alla coda per riproduzione
                        self.audio_queue.put_nowait(message)
                    except queue.Full:
                        # Coda piena, scarta il frame più vecchio
                        try:
                            self.audio_queue.get_nowait()
                            self.audio_queue.put_nowait(message)
                        except queue.Empty:
                            pass
                elif isinstance(message, str):
                    # Messaggio di testo
                    try:
                        data = json.loads(message)
                        if data.get("type") == "welcome":
                            print(f"✓ {data.get('message')}")
                    except:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ← Messaggio: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connessione chiusa dal server")
            self.connected = False
        except Exception as e:
            print(f"Errore nella ricezione: {e}")
            self.connected = False
    
    async def disconnect(self):
        """Disconnette dal server e chiude audio"""
        self.connected = False
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
        
        if self.websocket:
            await self.websocket.close()
        
        print("Disconnesso dal server e audio chiuso")

async def main():
    """Funzione principale"""
    client = MacBookAudioClient()
    
    # Connessione
    if not await client.connect():
        print("Impossibile connettersi. Uscita.")
        return
    
    # Inizializza audio
    if not client.init_audio():
        print("Impossibile inizializzare audio. Uscita.")
        await client.disconnect()
        return
    
    # Avvia thread per riproduzione audio
    audio_thread = threading.Thread(target=client.play_audio, daemon=True)
    audio_thread.start()
    
    # Task per ricevere audio in background
    receive_task = asyncio.create_task(client.receive_audio())
    
    print("\n" + "="*60)
    print("Client Audio WebSocket MacBook M2")
    print("="*60)
    print("In ricezione audio dall'ESP32...")
    print("Premi Ctrl+C per uscire")
    print("="*60 + "\n")
    
    try:
        # Mantieni il programma in esecuzione
        await receive_task
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta...")
    finally:
        # Cleanup
        receive_task.cancel()
        await client.disconnect()
        print("Uscita completata.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgramma terminato.")

