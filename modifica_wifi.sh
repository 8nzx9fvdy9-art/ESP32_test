#!/bin/bash
# Script per modificare facilmente WiFi SSID e Password

echo "📶 Modifica Configurazione WiFi"
echo ""

# Chiedi SSID
read -p "Inserisci il nome della rete WiFi (SSID): " WIFI_SSID

# Chiedi password (senza mostrarla)
read -sp "Inserisci la password WiFi: " WIFI_PASSWORD
echo ""

# Verifica che sdkconfig esista
if [ ! -f "sdkconfig" ]; then
    echo "❌ File sdkconfig non trovato!"
    echo "Esegui prima: idf.py menuconfig"
    exit 1
fi

# Backup del file originale
cp sdkconfig sdkconfig.backup

# Modifica sdkconfig
if grep -q "^CONFIG_WIFI_SSID=" sdkconfig; then
    # Sostituisci la riga esistente (usa un separatore diverso per evitare problemi con /)
    sed -i '' "s|^CONFIG_WIFI_SSID=.*|CONFIG_WIFI_SSID=\"$WIFI_SSID\"|" sdkconfig
    echo "✅ SSID aggiornato: $WIFI_SSID"
else
    # Aggiungi nuova riga
    echo "CONFIG_WIFI_SSID=\"$WIFI_SSID\"" >> sdkconfig
    echo "✅ SSID aggiunto: $WIFI_SSID"
fi

if grep -q "^CONFIG_WIFI_PASSWORD=" sdkconfig; then
    # Sostituisci la riga esistente
    sed -i '' "s|^CONFIG_WIFI_PASSWORD=.*|CONFIG_WIFI_PASSWORD=\"$WIFI_PASSWORD\"|" sdkconfig
    echo "✅ Password aggiornata: [nascosta]"
else
    # Aggiungi nuova riga
    echo "CONFIG_WIFI_PASSWORD=\"$WIFI_PASSWORD\"" >> sdkconfig
    echo "✅ Password aggiunta: [nascosta]"
fi

echo ""
echo "✅ WiFi configurato con successo!"
echo ""
echo "📝 Per verificare, esegui:"
echo "   grep -i WIFI sdkconfig"
echo ""
echo "🚀 Ora puoi compilare e flashare:"
echo "   idf.py build"
echo "   idf.py -p /dev/cu.usbserial-0001 flash monitor"


