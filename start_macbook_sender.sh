#!/bin/bash
# Script per avviare rapidamente il client MacBook

RENDER_URL="https://esp32-test-q46k.onrender.com"

echo "🎵 Avvio client audio MacBook"
echo "=============================="
echo ""
echo "URL Render: $RENDER_URL"
echo ""
echo "⚠️  Assicurati che:"
echo "   - BlackHole sia installato e selezionato come output audio"
echo "   - ffmpeg sia installato (brew install ffmpeg)"
echo ""

# Verifica che ffmpeg sia installato
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg non trovato!"
    echo "   Installa con: brew install ffmpeg"
    exit 1
fi

# Verifica che il file esista
if [ ! -f "macbook_audio_sender.py" ]; then
    echo "❌ File macbook_audio_sender.py non trovato!"
    exit 1
fi

# Verifica connessione al server
echo "🔍 Verifica connessione al server Render..."
if curl -s -f "$RENDER_URL/status" > /dev/null; then
    echo "✅ Server Render raggiungibile"
else
    echo "⚠️  Impossibile raggiungere il server Render"
    echo "   Verifica che il server sia online su: $RENDER_URL"
    read -p "Continuare comunque? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🚀 Avvio client audio..."
echo "   Premi Ctrl+C per fermare"
echo ""

python3 macbook_audio_sender.py --render-url "$RENDER_URL"

