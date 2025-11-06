#!/usr/bin/env python3
"""
Server WebSocket per Render.com
Questo server è ottimizzato per Render e supporta WebSocket nativamente
Gestisce anche health checks HTTP (HEAD/GET) per Render
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Set
from aiohttp import web
from aiohttp.web_ws import WebSocketResponse

# Set per tenere traccia delle connessioni WebSocket
clients: Set[WebSocketResponse] = set()

async def register_client(websocket):
    """Registra un nuovo client"""
    clients.add(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Nuovo client connesso. Totale: {len(clients)}")

async def unregister_client(websocket):
    """Rimuove un client disconnesso"""
    clients.discard(websocket)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnesso. Totale: {len(clients)}")

async def broadcast_message(message: str, sender: WebSocketResponse):
    """Invia un messaggio a tutti i client tranne il mittente"""
    if len(clients) < 2:
        # Serve almeno un altro client per comunicare
        return
    
    disconnected = set()
    for client in clients:
        if client != sender and not client.closed:
            try:
                await client.send_str(message)
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Errore nell'invio: {e}")
                disconnected.add(client)
    
    # Rimuovi client disconnessi
    for client in disconnected:
        await unregister_client(client)

async def websocket_handler(request):
    """Gestisce le connessioni WebSocket"""
    ws = WebSocketResponse()
    await ws.prepare(request)
    
    await register_client(ws)
    
    try:
        # Invia messaggio di benvenuto
        welcome_msg = json.dumps({
            "type": "welcome",
            "message": "Connesso al server WebSocket",
            "timestamp": datetime.now().isoformat()
        })
        await ws.send_str(welcome_msg)
        
        # Ricevi e inoltra messaggi
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                message = msg.data
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Messaggio ricevuto: {message}")
                
                # Inoltra a tutti gli altri client
                await broadcast_message(message, ws)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Errore WebSocket: {ws.exception()}")
                break
                
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Errore nel client: {e}")
    finally:
        await unregister_client(ws)
    
    return ws

async def root_handler(request):
    """Gestisce le richieste sulla root: HTTP health checks o WebSocket"""
    # Se è una richiesta WebSocket upgrade, gestiscila come WebSocket
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return await websocket_handler(request)
    
    # Altrimenti, è una richiesta HTTP normale (HEAD/GET per health checks)
    # Render fa health checks con richieste HEAD
    return web.Response(
        text="WebSocket Server is running",
        status=200,
        headers={"Content-Type": "text/plain"}
    )

if __name__ == "__main__":
    # Render usa la variabile d'ambiente PORT, altrimenti usa 8765
    port = int(os.environ.get("PORT", 8765))
    host = "0.0.0.0"  # Ascolta su tutte le interfacce
    
    print("="*60)
    print("Server WebSocket per ESP32 <-> MacBook")
    print("="*60)
    print(f"Server in ascolto su ws://{host}:{port}")
    print(f"Health checks HTTP su http://{host}:{port}/")
    print("Premi Ctrl+C per fermare il server")
    print("="*60)
    
    # Crea applicazione aiohttp
    app = web.Application()
    
    # Route sulla root: gestisce sia HTTP health checks che WebSocket
    # Nota: add_get registra automaticamente anche HEAD per health checks
    app.router.add_get('/', root_handler)
    
    # Route alternativa per WebSocket su /ws
    app.router.add_get('/ws', websocket_handler)
    
    # Avvia server (web.run_app gestisce già l'event loop)
    print("Server avviato. In attesa di connessioni...")
    try:
        web.run_app(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\nServer fermato.")
