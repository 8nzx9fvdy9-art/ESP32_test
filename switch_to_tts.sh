#!/bin/bash
# Script per passare automaticamente alla modalità TTS Server

echo "🔄 Passaggio alla modalità TTS Server..."

cd "$(dirname "$0")/main"

# Backup del file originale
cp CMakeLists.txt CMakeLists.txt.backup

# Cambia al server TTS
sed -i '' 's/^# set(COMPONENT_SRCS \.\/tts_server_example.c)/set(COMPONENT_SRCS .\/tts_server_example.c)/' CMakeLists.txt
sed -i '' 's/^set(COMPONENT_SRCS \.\/play_mp3_control_example.c)/# set(COMPONENT_SRCS .\/play_mp3_control_example.c)/' CMakeLists.txt

echo "✅ Cambiato a TTS Server mode"
echo "📝 Ora puoi compilare con: idf.py build"


