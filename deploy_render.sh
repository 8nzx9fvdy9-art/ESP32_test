#!/bin/bash
# Script per deploy automatico su Render

set -e

echo "🚀 Deploy Server Render"
echo "======================"
echo ""

# Verifica che i file necessari esistano
echo "📋 Verifica file necessari..."
REQUIRED_FILES=("render_server.py" "requirements.txt" "Procfile")

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ File mancante: $file"
        exit 1
    fi
    echo "✅ $file"
done

echo ""
echo "📦 Preparazione deploy..."

# Verifica se render CLI è installato
if ! command -v render &> /dev/null; then
    echo "⚠️  Render CLI non trovato"
    echo ""
    echo "Installa Render CLI:"
    echo "  brew install render"
    echo ""
    echo "Oppure usa il deploy manuale:"
    echo "  1. Vai su https://dashboard.render.com"
    echo "  2. Crea nuovo Web Service"
    echo "  3. Collega repository GitHub o carica i file"
    echo "  4. Build Command: pip install -r requirements.txt"
    echo "  5. Start Command: gunicorn render_server:app --bind 0.0.0.0:\$PORT --workers 2 --threads 2 --timeout 120"
    echo ""
    exit 1
fi

echo "✅ Render CLI trovato"
echo ""

# Login a Render (se necessario)
echo "🔐 Verifica login Render..."
if ! render whoami &> /dev/null; then
    echo "⚠️  Non sei loggato. Esegui: render login"
    exit 1
fi

echo "✅ Loggato in Render"
echo ""

# Crea o aggiorna servizio
SERVICE_NAME="esp32-test-q46k"
echo "🔧 Deploy servizio: $SERVICE_NAME"
echo ""

# Crea servizio se non esiste
if ! render services list | grep -q "$SERVICE_NAME"; then
    echo "📝 Creazione nuovo servizio..."
    render services create web \
        --name "$SERVICE_NAME" \
        --env python \
        --buildCommand "pip install -r requirements.txt" \
        --startCommand "gunicorn render_server:app --bind 0.0.0.0:\$PORT --workers 2 --threads 2 --timeout 120" \
        --region oregon \
        --plan free
else
    echo "✅ Servizio già esistente"
fi

echo ""
echo "✅ Deploy completato!"
echo ""
echo "🌐 URL servizio: https://$SERVICE_NAME.onrender.com"
echo ""
echo "📊 Monitora il deploy:"
echo "   render services logs $SERVICE_NAME"
echo ""

