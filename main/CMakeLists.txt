# =====================================================
# ESP32-A1S - Selezione esempio
# =====================================================
# Scegli quale esempio compilare:
# - play_mp3_control_example.c: Riproduzione MP3 da SD card
# - tts_server_example.c: Server TTS HTTP per ricevere e riprodurre audio
# - render_audio_receiver.c: Riceve stream audio da server Render
# =====================================================

set(COMPONENT_SRCS ./render_audio_receiver.c)
# set(COMPONENT_SRCS ./tts_server_example.c)
# set(COMPONENT_SRCS ./play_mp3_control_example.c)

set(COMPONENT_ADD_INCLUDEDIRS "")

# File audio di esempio inclusi nel firmware
set(COMPONENT_EMBED_TXTFILES
    music-16b-2c-8000hz.mp3
    music-16b-2c-22050hz.mp3
    music-16b-2c-44100hz.mp3
)

register_component()