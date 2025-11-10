#!/bin/bash
# Script per configurare rapidamente l'URL del server Render

RENDER_URL="https://esp32-test-q46k.onrender.com"

echo "🔧 Configurazione Render Server per ESP32"
echo "=========================================="
echo ""
echo "URL Render: $RENDER_URL"
echo ""

# Verifica che sdkconfig esista
if [ ! -f "sdkconfig" ]; then
    echo "⚠️  File sdkconfig non trovato. Eseguo menuconfig per crearlo..."
    idf.py menuconfig
fi

# Aggiungi o aggiorna CONFIG_RENDER_SERVER_URL
if grep -q "CONFIG_RENDER_SERVER_URL" sdkconfig; then
    # Aggiorna URL esistente
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|CONFIG_RENDER_SERVER_URL=.*|CONFIG_RENDER_SERVER_URL=\"$RENDER_URL\"|" sdkconfig
    else
        # Linux
        sed -i "s|CONFIG_RENDER_SERVER_URL=.*|CONFIG_RENDER_SERVER_URL=\"$RENDER_URL\"|" sdkconfig
    fi
    echo "✅ URL Render aggiornato in sdkconfig"
else
    # Aggiungi nuova configurazione
    echo "" >> sdkconfig
    echo "# Render Server URL" >> sdkconfig
    echo "CONFIG_RENDER_SERVER_URL=\"$RENDER_URL\"" >> sdkconfig
    echo "✅ URL Render aggiunto a sdkconfig"
fi

echo ""
echo "✅ Configurazione completata!"
echo ""
echo "Prossimi passi:"
echo "1. Verifica WiFi in menuconfig: idf.py menuconfig"
echo "2. Compila e flasha: idf.py build flash monitor"
echo "3. Avvia il client MacBook:"
echo "   python3 macbook_audio_sender.py --render-url $RENDER_URL"
echo ""

