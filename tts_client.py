#!/usr/bin/env python3
"""
Client Python per inviare testo all'ESP32 TTS Server
Genera audio con Google TTS (gTTS) e lo invia all'ESP32 per la riproduzione

Requisiti:
    pip install gtts requests

Utilizzo:
    python tts_client.py "Ciao, questo è un test"
    python tts_client.py --esp32-ip 192.168.1.100 "Ciao mondo"
    python tts_client.py --interactive  # Modalità interattiva
"""

import argparse
import requests
import tempfile
import os
import sys
from gtts import gTTS
import json

# Configurazione di default
DEFAULT_ESP32_IP = "192.168.1.100"  # Cambia con l'IP del tuo ESP32
DEFAULT_PORT = 80
DEFAULT_LANG = "it"  # Italiano
DEFAULT_TLD = "com"  # Top-level domain per gTTS

def generate_audio(text, lang="it", tld="com", output_file=None):
    """Genera file audio MP3 da testo usando Google TTS"""
    if output_file is None:
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_file.close()
        output_file = output_file.name
    
    print(f"Generando audio per: '{text}'")
    print(f"Lingua: {lang}, TLD: {tld}")
    
    try:
        tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
        tts.save(output_file)
        print(f"Audio generato: {output_file}")
        return output_file
    except Exception as e:
        print(f"Errore durante la generazione audio: {e}")
        return None

def start_local_server(audio_file, port=8080):
    """Avvia un server HTTP locale per servire il file audio"""
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading
    import socket
    
    # Ottieni l'IP locale della rete WiFi
    def get_local_ip():
        try:
            # Crea un socket UDP per trovare l'IP locale
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Non invia dati, ma determina l'IP locale
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            try:
                # Fallback: usa gethostbyname
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                if local_ip.startswith("127."):
                    # Se è localhost, prova a trovare un IP di rete
                    return None
                return local_ip
            except:
                return "127.0.0.1"
    
    local_ip = get_local_ip()
    if not local_ip or local_ip == "127.0.0.1":
        print("⚠️  Impossibile determinare l'IP locale. Usa l'IP del MacBook sulla rete WiFi.")
        print("   Puoi trovarlo con: ifconfig | grep 'inet ' | grep -v 127.0.0.1")
        local_ip = "127.0.0.1"
    
    # Cambia nella directory del file audio
    audio_dir = os.path.dirname(os.path.abspath(audio_file))
    audio_filename = os.path.basename(audio_file)
    original_dir = os.getcwd()
    
    class AudioHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == f'/{audio_filename}' or self.path == f'/audio.mp3':
                self.send_response(200)
                self.send_header('Content-type', 'audio/mpeg')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(audio_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            pass  # Disabilita log
    
    os.chdir(audio_dir)
    server = HTTPServer(('0.0.0.0', port), AudioHandler)
    
    def serve():
        server.serve_forever()
    
    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    
    # URL locale (l'ESP32 deve essere sulla stessa rete)
    audio_url = f"http://{local_ip}:{port}/{audio_filename}"
    print(f"Server HTTP locale avviato su {audio_url}")
    
    os.chdir(original_dir)
    return audio_url, server

def upload_audio_to_server(audio_file, esp32_ip, port=80, use_local_server=True):
    """Carica file audio su un server temporaneo e invia URL all'ESP32"""
    # Leggi il file audio
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    # Opzione 1: Server HTTP locale (più semplice e affidabile)
    if use_local_server:
        try:
            print("\nAvvio server HTTP locale...")
            audio_url, server = start_local_server(audio_file, port=8080)
            print(f"✅ File disponibile su: {audio_url}")
            print("⚠️  Nota: MacBook e ESP32 devono essere sulla stessa rete WiFi")
            
            # Invia richiesta all'ESP32
            result = send_play_request(esp32_ip, port, audio_url)
            
            # Mantieni il server attivo per qualche secondo per permettere il download
            import time
            time.sleep(10)  # Attendi che l'ESP32 scarichi il file
            
            return result
        except Exception as e:
            print(f"Errore con server locale: {e}")
            print("Tentativo con servizi online...")
    
    # Opzione 2: Usa 0x0.st (alternativa a transfer.sh)
    try:
        print("\nCaricamento file su 0x0.st...")
        response = requests.post(
            'https://0x0.st',
            files={'file': (os.path.basename(audio_file), audio_data, 'audio/mpeg')},
            timeout=30
        )
        
        if response.status_code == 200:
            audio_url = response.text.strip()
            print(f"✅ File caricato: {audio_url}")
            return send_play_request(esp32_ip, port, audio_url)
        else:
            print(f"❌ Errore nel caricamento: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore con 0x0.st: {e}")
    
    # Opzione 3: Fallback a transfer.sh
    try:
        print("\nTentativo con transfer.sh...")
        response = requests.post(
            'https://transfer.sh/',
            files={'file': (os.path.basename(audio_file), audio_data, 'audio/mpeg')},
            headers={'Max-Downloads': '1', 'Max-Days': '1'},
            timeout=30
        )
        
        if response.status_code == 200:
            audio_url = response.text.strip()
            print(f"✅ File caricato: {audio_url}")
            return send_play_request(esp32_ip, port, audio_url)
        else:
            print(f"❌ Errore nel caricamento: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore con transfer.sh: {e}")
    
    print("\n❌ Tutti i metodi di upload hanno fallito.")
    print("💡 Suggerimento: Usa un server HTTP locale (--local-server) o configura Render")
    return False

def send_play_request(esp32_ip, port, audio_url):
    """Invia richiesta all'ESP32 per riprodurre audio da URL"""
    url = f"http://{esp32_ip}:{port}/play"
    
    # Prova prima con JSON nel body
    payload = {"url": audio_url}
    headers = {"Content-Type": "application/json"}
    
    print(f"\nInvio richiesta a: {url}")
    print(f"URL audio: {audio_url}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ Successo! {response.text}")
            return True
        else:
            print(f"❌ Errore: {response.status_code} - {response.text}")
            # Prova con query parameter
            print("Tentativo con query parameter...")
            response = requests.post(f"{url}?url={requests.utils.quote(audio_url)}", timeout=10)
            if response.status_code == 200:
                print(f"✅ Successo! {response.text}")
                return True
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione: {e}")
        print(f"   Assicurati che l'ESP32 sia connesso e raggiungibile su {esp32_ip}:{port}")
        return False

def send_text_direct(esp32_ip, port, text):
    """Invia testo direttamente all'ESP32 (per uso futuro con TTS su ESP32)"""
    url = f"http://{esp32_ip}:{port}/text"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Risposta: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Errore: {e}")
        return False

def interactive_mode(esp32_ip, port, lang, tld):
    """Modalità interattiva per inviare più testi"""
    print("\n" + "="*50)
    print("Modalità interattiva TTS")
    print("="*50)
    print(f"ESP32 IP: {esp32_ip}:{port}")
    print(f"Lingua: {lang}")
    print("Scrivi 'quit' o 'exit' per uscire")
    print("="*50 + "\n")
    
    while True:
        try:
            text = input("Inserisci testo da pronunciare: ").strip()
            
            if not text:
                continue
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("Arrivederci!")
                break
            
            # Genera audio
            audio_file = generate_audio(text, lang, tld)
            if audio_file:
                # Invia all'ESP32 (usa server locale di default)
                upload_audio_to_server(audio_file, esp32_ip, port, use_local_server=True)
                
                # Pulisci file temporaneo dopo un delay
                import time
                time.sleep(2)
                try:
                    os.unlink(audio_file)
                except:
                    pass
        except KeyboardInterrupt:
            print("\nArrivederci!")
            break
        except Exception as e:
            print(f"Errore: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Client TTS per ESP32 - Invia testo e riproduce audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s "Ciao, questo è un test"
  %(prog)s --esp32-ip 192.168.1.50 "Hello world" --lang en
  %(prog)s --interactive
        """
    )
    
    parser.add_argument("text", nargs="?", help="Testo da pronunciare")
    parser.add_argument("--esp32-ip", default=DEFAULT_ESP32_IP,
                       help=f"Indirizzo IP dell'ESP32 (default: {DEFAULT_ESP32_IP})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                       help=f"Porta del server HTTP (default: {DEFAULT_PORT})")
    parser.add_argument("--lang", default=DEFAULT_LANG,
                       help=f"Lingua per TTS (default: {DEFAULT_LANG})")
    parser.add_argument("--tld", default=DEFAULT_TLD,
                       help=f"Top-level domain per gTTS (default: {DEFAULT_TLD})")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Modalità interattiva")
    parser.add_argument("--audio-file", help="Usa file audio esistente invece di generarlo")
    parser.add_argument("--local-server", action="store_true", default=True,
                       help="Usa server HTTP locale invece di servizi online (default: True)")
    parser.add_argument("--no-local-server", dest="local_server", action="store_false",
                       help="Non usare server HTTP locale, usa servizi online")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(args.esp32_ip, args.port, args.lang, args.tld)
    elif args.text:
        if args.audio_file:
            # Usa file audio esistente
            send_play_request(args.esp32_ip, args.port, args.audio_file)
        else:
            # Genera audio e invia
            audio_file = generate_audio(args.text, args.lang, args.tld)
            if audio_file:
                upload_audio_to_server(audio_file, args.esp32_ip, args.port, use_local_server=args.local_server)
                # Pulisci file temporaneo dopo un delay
                import time
                time.sleep(2)
                try:
                    os.unlink(audio_file)
                except:
                    pass
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

