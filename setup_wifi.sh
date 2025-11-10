#!/bin/bash
# Script per configurare WiFi in modo semplice

echo "📶 Configurazione WiFi per ESP32"
echo ""

# Chiedi SSID
read -p "Inserisci il nome della rete WiFi (SSID): " WIFI_SSID

# Chiedi password (senza mostrarla)
read -sp "Inserisci la password WiFi: " WIFI_PASSWORD
echo ""

# Verifica che sdkconfig esista
if [ ! -f "sdkconfig" ]; then
    echo "❌ File sdkconfig non trovato. Esegui prima: idf.py menuconfig"
    exit 1
fi

# Modifica sdkconfig usando idf.py menuconfig o modifica diretta
echo ""
echo "⚠️  Configurazione WiFi:"
echo ""
echo "Opzione 1 (Automatica):"
echo "  Esegui: idf.py menuconfig"
echo "  Vai su: Component config → TTS Server Configuration"
echo "  Imposta WiFi SSID e Password"
echo ""
echo "Opzione 2 (Manuale):"
echo "  Apri il file sdkconfig con un editor"
echo "  Cerca: CONFIG_WIFI_SSID"
echo "  Cambia in: CONFIG_WIFI_SSID=\"$WIFI_SSID\""
echo "  Cerca: CONFIG_WIFI_PASSWORD"
echo "  Cambia in: CONFIG_WIFI_PASSWORD=\"$WIFI_PASSWORD\""
echo ""
echo "Valori da inserire:"
echo "  SSID: $WIFI_SSID"
echo "  Password: [nascosta]"
echo ""
read -p "Premi Invio quando hai configurato il WiFi..."

echo "✅ WiFi configurato!"
echo "   SSID: $WIFI_SSID"
echo "   Password: [nascosta]"
echo ""
echo "📝 Ora puoi compilare e flashare con:"
echo "   idf.py build"
echo "   idf.py -p PORTA flash"

