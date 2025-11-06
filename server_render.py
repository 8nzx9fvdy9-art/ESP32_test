#!/usr/bin/env python3
"""
Server WebSocket per Render.com
Questo server è ottimizzato per Render e supporta WebSocket nativamente
"""

import asyncio
import websockets
import json
import os
from datetime import datetime
from typing import Set

# Set per tenere traccia delle connessioni
clients: Set[websockets.WebSocketServerProtocol] = set()

async def register_client(websocket):
    """Registra un nuovo client"""
    clients.add(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Nuovo client connesso. Totale: {len(clients)}")

async def unregister_client(websocket):
    """Rimuove un client disconnesso"""
    clients.discard(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnesso. Totale: {len(clients)}")

async def broadcast_message(message: str, sender: websockets.WebSocketServerProtocol):
    """Invia un messaggio a tutti i client tranne il mittente"""
    if len(clients) < 2:
        # Serve almeno un altro client per comunicare
        return
    
    disconnected = set()
    for client in clients:
        if client != sender and client.open:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
    
    # Rimuovi client disconnessi
    for client in disconnected:
        await unregister_client(client)

async def handle_client(websocket, path):
    """Gestisce la connessione di un client"""
    await register_client(websocket)
    
    try:
        # Invia messaggio di benvenuto
        welcome_msg = json.dumps({
            "type": "welcome",
            "message": "Connesso al server WebSocket",
            "timestamp": datetime.now().isoformat()
        })
        await websocket.send(welcome_msg)
        
        # Ricevi e inoltra messaggi
        # Nota: ping/pong è gestito automaticamente dal server (configurato in websockets.serve)
        async for message in websocket:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Messaggio ricevuto: {message}")
            
            # Inoltra a tutti gli altri client
            await broadcast_message(message, websocket)
            
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Errore nel client: {e}")
    finally:
        await unregister_client(websocket)

async def main():
    """Avvia il server WebSocket"""
    # Render usa la variabile d'ambiente PORT, altrimenti usa 8765
    port = int(os.environ.get("PORT", 8765))
    host = "0.0.0.0"  # Ascolta su tutte le interfacce
    
    print("="*60)
    print("Server WebSocket per ESP32 <-> MacBook")
    print("="*60)
    print(f"Server in ascolto su ws://{host}:{port}")
    print("Premi Ctrl+C per fermare il server")
    print("="*60)
    
    # Configura il server con ping/pong per mantenere le connessioni attive
    async with websockets.serve(
        handle_client, 
        host, 
        port,
        ping_interval=20,  # Ping ogni 20 secondi
        ping_timeout=10,   # Timeout di 10 secondi
        close_timeout=10   # Timeout di chiusura
    ):
        await asyncio.Future()  # Esegui indefinitamente

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer fermato.")

