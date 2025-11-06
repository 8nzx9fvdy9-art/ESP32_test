#!/usr/bin/env python3
"""
Client WebSocket per MacBook M2
Comunica con ESP32 tramite server WebSocket intermedio
"""

import asyncio
import websockets
import json
import sys
import threading
from datetime import datetime

# ===== CONFIGURAZIONE SERVER =====
# Deve essere lo stesso server usato dall'ESP32
WEBSOCKET_SERVER = "nonflatulent-colby-pearly.ngrok-free.dev"  # URL ngrok
WEBSOCKET_PORT = 443  # HTTPS usa porta 443
WEBSOCKET_PATH = "/"

# URL completo (usa wss:// per HTTPS, non ws://)
WEBSOCKET_URL = f"wss://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}{WEBSOCKET_PATH}"

class MacBookWebSocketClient:
    def __init__(self):
        self.websocket = None
        self.connected = False
        
    async def connect(self):
        """Connette al server WebSocket"""
        try:
            print(f"Connessione a {WEBSOCKET_URL}...")
            self.websocket = await websockets.connect(WEBSOCKET_URL)
            self.connected = True
            print("✓ Connesso al server WebSocket!")
            return True
        except Exception as e:
            print(f"✗ Errore di connessione: {e}")
            return False
    
    async def send_message(self, message):
        """Invia un messaggio all'ESP32 tramite server"""
        if not self.connected or not self.websocket:
            print("Non connesso, impossibile inviare messaggio")
            return False
        
        try:
            await self.websocket.send(message)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] → Inviato: {message}")
            return True
        except Exception as e:
            print(f"Errore nell'invio: {e}")
            self.connected = False
            return False
    
    async def receive_messages(self):
        """Riceve messaggi dall'ESP32 tramite server"""
        if not self.connected or not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] ← Ricevuto: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connessione chiusa dal server")
            self.connected = False
        except Exception as e:
            print(f"Errore nella ricezione: {e}")
            self.connected = False
    
    async def disconnect(self):
        """Disconnette dal server"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print("Disconnesso dal server")

async def main():
    """Funzione principale"""
    client = MacBookWebSocketClient()
    
    # Connessione
    if not await client.connect():
        print("Impossibile connettersi. Uscita.")
        return
    
    # Task per ricevere messaggi in background
    receive_task = asyncio.create_task(client.receive_messages())
    
    print("\n" + "="*50)
    print("Client WebSocket MacBook M2")
    print("="*50)
    print("Comandi:")
    print("  - Digita un messaggio e premi INVIO per inviarlo all'ESP32")
    print("  - Digita 'quit' o 'exit' per uscire")
    print("="*50 + "\n")
    
    try:
        # Loop principale: leggi input da terminale e invia
        input_queue = asyncio.Queue()
        input_running = threading.Event()
        input_running.set()  # Inizia come attivo
        
        def read_input():
            """Legge input da terminale in un thread separato"""
            while input_running.is_set():
                try:
                    user_input = input("> ").strip()
                    if user_input:
                        asyncio.run_coroutine_threadsafe(
                            input_queue.put(user_input),
                            asyncio.get_event_loop()
                        )
                except (EOFError, KeyboardInterrupt):
                    asyncio.run_coroutine_threadsafe(
                        input_queue.put("__QUIT__"),
                        asyncio.get_event_loop()
                    )
                    break
        
        # Avvia thread per leggere input
        input_thread = threading.Thread(target=read_input, daemon=True)
        input_thread.start()
        
        print("In attesa di input... (digita 'quit' per uscire)")
        
        while client.connected:
            try:
                # Attendi input con timeout
                user_input = await asyncio.wait_for(input_queue.get(), timeout=0.5)
                
                if user_input == "__QUIT__" or user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if user_input:
                    await client.send_message(f"MacBook dice: {user_input}")
            except asyncio.TimeoutError:
                # Timeout: continua il loop
                pass
                
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta...")
    finally:
        # Cleanup
        input_running.clear()
        receive_task.cancel()
        await client.disconnect()
        print("Uscita completata.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgramma terminato.")

