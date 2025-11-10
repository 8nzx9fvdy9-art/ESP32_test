#!/usr/bin/env python3
"""
Client MacBook per catturare audio di sistema e inviarlo al server Render
"""

import subprocess
import requests
import sys
import signal
import time
import argparse

class AudioCapture:
    def __init__(self, render_url, chunk_size=4096):
        self.render_url = render_url.rstrip('/')
        self.chunk_size = chunk_size
        self.ffmpeg_process = None
        self.running = False
        
    def start_capture(self):
        """Avvia la cattura audio usando ffmpeg"""
        print("Avvio cattura audio di sistema...")
        print("⚠️  Assicurati di aver installato BlackHole o Soundflower per catturare l'audio di sistema")
        print("   BlackHole: https://github.com/ExistentialAudio/BlackHole")
        
        # Comando ffmpeg per catturare audio di sistema
        # Su macOS, usa BlackHole come dispositivo virtuale
        # Prima configura macOS per usare BlackHole come output audio
        
        # Opzione 1: Cattura da BlackHole (dispositivo virtuale)
        # L'utente deve configurare macOS per usare BlackHole come output
        # Per trovare il device ID: ffmpeg -f avfoundation -list_devices true -i ""
        cmd = [
            'ffmpeg',
            '-f', 'avfoundation',  # macOS audio framework
            '-i', ':0',  # Cattura da dispositivo di default (BlackHole se configurato)
            '-f', 'mp3',  # Formato MP3
            '-acodec', 'libmp3lame',  # Codec MP3
            '-ar', '44100',  # Sample rate
            '-ac', '2',  # Stereo
            '-b:a', '128k',  # Bitrate
            '-'  # Output su stdout
        ]
        
        try:
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=self.chunk_size
            )
            self.running = True
            print("✅ Cattura audio avviata")
            return True
        except FileNotFoundError:
            print("❌ Errore: ffmpeg non trovato. Installa con: brew install ffmpeg")
            return False
        except Exception as e:
            print(f"❌ Errore avvio ffmpeg: {e}")
            return False
    
    def send_audio_loop(self):
        """Loop principale per inviare audio al server"""
        if not self.ffmpeg_process:
            print("❌ ffmpeg non avviato")
            return
        
        print(f"Invio audio a {self.render_url}/audio")
        print("Premi Ctrl+C per fermare")
        
        try:
            while self.running and self.ffmpeg_process.poll() is None:
                # Leggi chunk di audio
                chunk = self.ffmpeg_process.stdout.read(self.chunk_size)
                
                if not chunk:
                    time.sleep(0.1)
                    continue
                
                # Invia al server Render
                try:
                    response = requests.post(
                        f"{self.render_url}/audio",
                        data=chunk,
                        headers={'Content-Type': 'audio/mpeg'},
                        timeout=2
                    )
                    
                    if response.status_code != 200:
                        print(f"⚠️  Errore invio: {response.status_code}")
                    
                except requests.exceptions.RequestException as e:
                    print(f"⚠️  Errore connessione: {e}")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Interruzione richiesta...")
        finally:
            self.stop()
    
    def stop(self):
        """Ferma la cattura audio"""
        self.running = False
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            try:
                self.ffmpeg_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ffmpeg_process.kill()
            print("✅ Cattura audio fermata")

def main():
    parser = argparse.ArgumentParser(description='Invia audio MacBook al server Render')
    parser.add_argument('--render-url', 
                       default='http://localhost:5000',
                       help='URL del server Render (default: http://localhost:5000)')
    parser.add_argument('--chunk-size', 
                       type=int, 
                       default=4096,
                       help='Dimensione chunk audio in bytes (default: 4096)')
    
    args = parser.parse_args()
    
    # Verifica che ffmpeg sia installato
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ ffmpeg non trovato o non funzionante")
        print("   Installa con: brew install ffmpeg")
        sys.exit(1)
    
    # Verifica connessione al server
    try:
        response = requests.get(f"{args.render_url}/status", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server Render raggiungibile: {args.render_url}")
        else:
            print(f"⚠️  Server risponde con codice {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Impossibile connettersi al server: {e}")
        print(f"   Assicurati che il server sia avviato su {args.render_url}")
        sys.exit(1)
    
    # Avvia cattura e invio
    capture = AudioCapture(args.render_url, args.chunk_size)
    
    if not capture.start_capture():
        sys.exit(1)
    
    # Gestione segnale per cleanup
    def signal_handler(sig, frame):
        capture.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Loop principale
    capture.send_audio_loop()

if __name__ == '__main__':
    main()

