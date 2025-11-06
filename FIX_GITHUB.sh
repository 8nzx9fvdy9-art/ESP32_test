#!/bin/bash
# Script per configurare GitHub per Render

echo "🔧 Configurazione GitHub per Render"
echo "=================================="
echo ""

# Chiedi username GitHub
read -p "Inserisci il tuo username GitHub: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username GitHub non può essere vuoto!"
    exit 1
fi

# Aggiorna remote
echo ""
echo "📝 Aggiornamento remote GitHub..."
git remote set-url origin "https://github.com/${GITHUB_USERNAME}/ESP32_test.git"

# Verifica remote
echo ""
echo "✅ Remote aggiornato:"
git remote -v

# Rinomina branch a main (se necessario)
echo ""
echo "📝 Rinomina branch a main..."
git branch -M main

# Push
echo ""
echo "📤 Push su GitHub..."
git push -u origin main

echo ""
echo "✅ Fatto! Ora puoi usare Render.com"
echo ""
echo "Prossimi passi:"
echo "1. Vai su https://render.com"
echo "2. Crea nuovo Web Service"
echo "3. Connetti repository: https://github.com/${GITHUB_USERNAME}/ESP32_test"
echo "4. Deploy automatico!"

