#!/bin/bash
# Script per tornare alla modalità SD card

echo "🔄 Passaggio alla modalità SD Card..."

cd "$(dirname "$0")/main"

# Ripristina il file originale
cp CMakeLists.txt.backup CMakeLists.txt 2>/dev/null || true

# Cambia a SD card mode
sed -i '' 's/^set(COMPONENT_SRCS \.\/tts_server_example.c)/# set(COMPONENT_SRCS .\/tts_server_example.c)/' CMakeLists.txt
sed -i '' 's/^# set(COMPONENT_SRCS \.\/play_mp3_control_example.c)/set(COMPONENT_SRCS .\/play_mp3_control_example.c)/' CMakeLists.txt

echo "✅ Cambiato a SD Card mode"
echo "📝 Ora puoi compilare con: idf.py build"


