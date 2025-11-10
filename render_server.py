#!/usr/bin/env python3
"""
Server Render per streaming audio MacBook -> ESP32
Riceve audio dal MacBook e lo streama all'ESP32
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import io
import os
import threading
import queue
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permette richieste cross-origin

# Buffer circolare per lo streaming audio
audio_buffer = queue.Queue(maxsize=50)  # Buffer fino a 50 chunk
buffer_lock = threading.Lock()
last_audio_time = None
STREAM_TIMEOUT = 5  # Secondi di timeout per lo stream

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "endpoints": {
            "POST /audio": "Invia audio dal MacBook (Content-Type: audio/mpeg o audio/wav)",
            "GET /stream": "Ricevi stream audio per ESP32",
            "GET /status": "Stato del server"
        }
    })

@app.route('/status', methods=['GET'])
def status():
    with buffer_lock:
        buffer_size = audio_buffer.qsize()
        is_active = last_audio_time and (time.time() - last_audio_time) < STREAM_TIMEOUT
    
    return jsonify({
        "status": "online",
        "buffer_size": buffer_size,
        "stream_active": is_active,
        "last_audio_time": last_audio_time
    })

@app.route('/audio', methods=['POST'])
def receive_audio():
    """Riceve audio dal MacBook"""
    global last_audio_time
    
    try:
        # Leggi i dati audio
        audio_data = request.data
        
        if not audio_data:
            return jsonify({"error": "No audio data received"}), 400
        
        # Aggiungi al buffer
        with buffer_lock:
            # Rimuovi vecchi chunk se il buffer è pieno
            while audio_buffer.full():
                try:
                    audio_buffer.get_nowait()
                except queue.Empty:
                    break
            
            audio_buffer.put(audio_data)
            last_audio_time = time.time()
        
        print(f"[{datetime.now()}] Received {len(audio_data)} bytes of audio, buffer size: {audio_buffer.qsize()}")
        
        return jsonify({
            "status": "received",
            "size": len(audio_data),
            "buffer_size": audio_buffer.qsize()
        }), 200
        
    except Exception as e:
        print(f"Error receiving audio: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stream', methods=['GET'])
def stream_audio():
    """Streama audio all'ESP32"""
    print(f"[{datetime.now()}] ESP32 connected for streaming")
    
    def generate():
        global last_audio_time
        consecutive_empty = 0
        max_empty = 10  # Numero massimo di chunk vuoti consecutivi
        
        while True:
            try:
                # Controlla se c'è audio recente
                with buffer_lock:
                    if last_audio_time and (time.time() - last_audio_time) > STREAM_TIMEOUT:
                        print("Stream timeout - no audio received recently")
                        break
                
                # Prova a ottenere un chunk di audio
                try:
                    chunk = audio_buffer.get(timeout=0.5)
                    consecutive_empty = 0
                    yield chunk
                except queue.Empty:
                    consecutive_empty += 1
                    if consecutive_empty >= max_empty:
                        print("Stream ended - no more audio")
                        break
                    # Invia chunk vuoto per mantenere la connessione
                    time.sleep(0.1)
                    continue
                    
            except Exception as e:
                print(f"Error in stream generator: {e}")
                break
    
    return Response(
        generate(),
        mimetype='audio/mpeg',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

if __name__ == '__main__':
    print("Starting Render Audio Streaming Server...")
    print("Endpoints:")
    print("  POST /audio - Receive audio from MacBook")
    print("  GET /stream - Stream audio to ESP32")
    print("  GET /status - Server status")
    
    # Su Render, usa la porta da variabile d'ambiente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)

