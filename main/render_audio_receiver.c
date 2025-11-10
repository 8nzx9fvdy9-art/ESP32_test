/* Render Audio Receiver per ESP32-A1S
 * Si connette al server Render e riceve stream audio continuo
 * 
 * Questo esempio code is in the Public Domain (or CC0 licensed, at your option.)
 */

#include <string.h>
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_netif_types.h"
#include "esp_wifi_types.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include "lwip/inet.h"
#include "lwip/ip4_addr.h"
#include "esp_netif_ip_addr.h"
#include "sdkconfig.h"
#include "audio_element.h"
#include "audio_pipeline.h"
#include "audio_event_iface.h"
#include "audio_common.h"
#include "http_stream.h"
#include "i2s_stream.h"
#include "mp3_decoder.h"
#include "esp_peripherals.h"
#include "periph_wifi.h"
#include "board.h"

static const char *TAG = "RENDER_AUDIO";

// Pipeline globale per riproduzione audio
static audio_pipeline_handle_t g_audio_pipeline = NULL;
static audio_element_handle_t g_http_stream_reader = NULL;
static audio_element_handle_t g_mp3_decoder = NULL;
static audio_element_handle_t g_i2s_stream_writer = NULL;
static audio_board_handle_t g_board_handle = NULL;
static TaskHandle_t g_playback_task = NULL;
static audio_event_iface_handle_t g_audio_evt = NULL;

// URL del server Render (configurabile via menuconfig)
// Usa CONFIG_RENDER_SERVER_URL da menuconfig

// Task per gestire la riproduzione audio
static void audio_playback_task(void *pvParameters)
{
    ESP_LOGI(TAG, "Audio playback task started");
    
    while (1) {
        if (g_audio_evt == NULL) {
            vTaskDelay(pdMS_TO_TICKS(100));
            continue;
        }
        
        audio_event_iface_msg_t msg;
        esp_err_t ret = audio_event_iface_listen(g_audio_evt, &msg, pdMS_TO_TICKS(100));
        
        if (ret != ESP_OK) {
            continue;
        }
        
        // Gestione informazioni audio dal decoder MP3
        if (msg.source_type == AUDIO_ELEMENT_TYPE_ELEMENT
            && msg.source == (void *) g_mp3_decoder
            && msg.cmd == AEL_MSG_CMD_REPORT_MUSIC_INFO) {
            audio_element_info_t music_info = {0};
            audio_element_getinfo(g_mp3_decoder, &music_info);
            
            ESP_LOGI(TAG, "Music info: sample_rates=%d, bits=%d, ch=%d",
                     music_info.sample_rates, music_info.bits, music_info.channels);
            
            i2s_stream_set_clk(g_i2s_stream_writer, 
                              music_info.sample_rates, 
                              music_info.bits, 
                              music_info.channels);
            ESP_LOGI(TAG, "I2S clock configured: %d Hz, %d bit, %d channels", 
                     music_info.sample_rates, music_info.bits, music_info.channels);
            
            // Assicurati che il volume sia impostato anche durante la riproduzione
            if (g_board_handle && g_board_handle->audio_hal) {
                audio_hal_set_mute(g_board_handle->audio_hal, false);
            }
            continue;
        }
        
        // Se lo stream si interrompe, riconnetti
        if (msg.source_type == AUDIO_ELEMENT_TYPE_ELEMENT 
            && msg.source == (void *) g_http_stream_reader
            && msg.cmd == AEL_MSG_CMD_REPORT_STATUS
            && ((int)msg.data == AEL_STATUS_STATE_STOPPED 
                || (int)msg.data == AEL_STATUS_STATE_FINISHED)) {
            ESP_LOGW(TAG, "Stream interrupted, reconnecting...");
            vTaskDelay(pdMS_TO_TICKS(1000));
            
            // Riconnetti allo stream
            char stream_url[256];
            snprintf(stream_url, sizeof(stream_url), "%s/stream", CONFIG_RENDER_SERVER_URL);
            audio_element_set_uri(g_http_stream_reader, stream_url);
            audio_pipeline_run(g_audio_pipeline);
        }
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "Starting Render Audio Receiver...");
    
    // Inizializza NVS
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK(err);
    
    // Inizializza networking
    ESP_ERROR_CHECK(esp_netif_init());
    
    // Inizializza audio board
    ESP_LOGI(TAG, "[1] Start audio codec chip");
    g_board_handle = audio_board_init();
    if (g_board_handle && g_board_handle->audio_hal) {
        audio_hal_ctrl_codec(g_board_handle->audio_hal, AUDIO_HAL_CODEC_MODE_DECODE, AUDIO_HAL_CTRL_START);
        
        // Imposta il volume (0-100)
        int volume = 70;  // Volume al 70%
        ESP_LOGI(TAG, "[1.1] Setting volume to %d%%", volume);
        audio_hal_set_volume(g_board_handle->audio_hal, volume);
        
        // Verifica che il volume sia stato impostato
        int actual_volume = 0;
        audio_hal_get_volume(g_board_handle->audio_hal, &actual_volume);
        ESP_LOGI(TAG, "[1.2] Volume set to %d%%", actual_volume);
        
        // Assicurati che non sia in mute
        audio_hal_set_mute(g_board_handle->audio_hal, false);
        ESP_LOGI(TAG, "[1.3] Audio unmuted");
    } else {
        ESP_LOGW(TAG, "[1] Audio HAL not available, continuing without hardware codec");
    }
    
    // Crea pipeline audio
    ESP_LOGI(TAG, "[2] Create audio pipeline");
    audio_pipeline_cfg_t pipeline_cfg = DEFAULT_AUDIO_PIPELINE_CONFIG();
    g_audio_pipeline = audio_pipeline_init(&pipeline_cfg);
    mem_assert(g_audio_pipeline);
    
    // Crea HTTP stream reader
    ESP_LOGI(TAG, "[3] Create HTTP stream");
    http_stream_cfg_t http_cfg = HTTP_STREAM_CFG_DEFAULT();
    g_http_stream_reader = http_stream_init(&http_cfg);
    
    // Crea MP3 decoder
    ESP_LOGI(TAG, "[4] Create MP3 decoder");
    mp3_decoder_cfg_t mp3_cfg = DEFAULT_MP3_DECODER_CONFIG();
    g_mp3_decoder = mp3_decoder_init(&mp3_cfg);
    
    // Crea I2S stream writer
    ESP_LOGI(TAG, "[5] Create I2S stream");
    i2s_stream_cfg_t i2s_cfg = I2S_STREAM_CFG_DEFAULT();
    i2s_cfg.type = AUDIO_STREAM_WRITER;
    g_i2s_stream_writer = i2s_stream_init(&i2s_cfg);
    
    // Registra elementi nella pipeline
    ESP_LOGI(TAG, "[6] Register pipeline elements");
    audio_pipeline_register(g_audio_pipeline, g_http_stream_reader, "http");
    audio_pipeline_register(g_audio_pipeline, g_mp3_decoder, "mp3");
    audio_pipeline_register(g_audio_pipeline, g_i2s_stream_writer, "i2s");
    
    // Collega pipeline: http -> mp3 -> i2s
    ESP_LOGI(TAG, "[7] Link pipeline");
    const char *link_tag[3] = {"http", "mp3", "i2s"};
    audio_pipeline_link(g_audio_pipeline, &link_tag[0], 3);
    
    // Configura event listener
    ESP_LOGI(TAG, "[8] Setup event listener");
    audio_event_iface_cfg_t evt_cfg = AUDIO_EVENT_IFACE_DEFAULT_CFG();
    g_audio_evt = audio_event_iface_init(&evt_cfg);
    audio_pipeline_set_listener(g_audio_pipeline, g_audio_evt);
    
    // Avvia task per gestire riproduzione audio
    xTaskCreate(audio_playback_task, "audio_playback", 4096, NULL, 5, &g_playback_task);
    
    // Configura e connetti WiFi
    ESP_LOGI(TAG, "[9] Start WiFi");
    esp_periph_config_t periph_cfg = DEFAULT_ESP_PERIPH_SET_CONFIG();
    esp_periph_set_handle_t set = esp_periph_set_init(&periph_cfg);
    
    periph_wifi_cfg_t wifi_cfg = {
        .wifi_config.sta.ssid = CONFIG_WIFI_SSID,
        .wifi_config.sta.password = CONFIG_WIFI_PASSWORD,
    };
    esp_periph_handle_t wifi_handle = periph_wifi_init(&wifi_cfg);
    esp_periph_start(set, wifi_handle);
    periph_wifi_wait_for_connected(wifi_handle, portMAX_DELAY);
    
    // Ottieni indirizzo IP
    esp_netif_ip_info_t ip_info;
    esp_netif_t *netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
    if (netif) {
        esp_netif_get_ip_info(netif, &ip_info);
        ESP_LOGI(TAG, "WiFi connected! IP address: " IPSTR, IP2STR(&ip_info.ip));
    } else {
        ESP_LOGW(TAG, "WiFi connected but could not get IP address");
    }
    
    // Connessione al server Render
    ESP_LOGI(TAG, "[10] Connect to Render server");
    char stream_url[256];
    snprintf(stream_url, sizeof(stream_url), "%s/stream", CONFIG_RENDER_SERVER_URL);
    ESP_LOGI(TAG, "Stream URL: %s", stream_url);
    
    // Configura l'URL dello stream
    audio_element_set_uri(g_http_stream_reader, stream_url);
    
    // Breve delay per assicurarsi che tutto sia pronto
    vTaskDelay(pdMS_TO_TICKS(1000));
    
    // Avvia la pipeline
    ESP_LOGI(TAG, "[11] Starting audio stream...");
    audio_pipeline_run(g_audio_pipeline);
    
    ESP_LOGI(TAG, "✅ Render Audio Receiver ready!");
    ESP_LOGI(TAG, "Listening for audio stream from: %s", CONFIG_RENDER_SERVER_URL);
    
    // Loop principale
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

