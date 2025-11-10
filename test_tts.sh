#!/bin/bash
# Script helper per testare il TTS senza problemi con le virgolette

ESP32_IP="${1:-192.168.0.85}"
TEXT="${2:-Ciao, questo è un test!}"

echo "📤 Invio testo all'ESP32..."
echo "   IP: $ESP32_IP"
echo "   Testo: $TEXT"
echo ""

python3 tts_client.py --esp32-ip "$ESP32_IP" "$TEXT"


