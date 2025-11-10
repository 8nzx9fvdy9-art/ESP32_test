/* Text-to-Speech Server per ESP32-A1S
 * Riceve testo/audio via HTTP e lo riproduce tramite I2S
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
#include "esp_http_server.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_netif_types.h"
#include "esp_wifi_types.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include "lwip/inet.h"
#include "lwip/ip4_addr.h"
#include "esp_netif_ip_addr.h"
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

static const char *TAG = "TTS_SERVER";

// Pipeline globale per riproduzione audio
static audio_pipeline_handle_t g_audio_pipeline = NULL;
static audio_element_handle_t g_http_stream_reader = NULL;
static audio_element_handle_t g_mp3_decoder = NULL;
static audio_element_handle_t g_i2s_stream_writer = NULL;
static audio_board_handle_t g_board_handle = NULL;
static TaskHandle_t g_playback_task = NULL;
static audio_event_iface_handle_t g_audio_evt = NULL;

// Mutex per sincronizzare accesso alla pipeline
static SemaphoreHandle_t g_pipeline_mutex = NULL;

// Funzione per fermare e pulire la pipeline audio
static void stop_audio_pipeline(void)
{
    if (g_audio_pipeline == NULL) return;
    
    xSemaphoreTake(g_pipeline_mutex, portMAX_DELAY);
    
    ESP_LOGI(TAG, "Stopping audio pipeline");
    audio_pipeline_stop(g_audio_pipeline);
    audio_pipeline_wait_for_stop(g_audio_pipeline);
    audio_pipeline_terminate(g_audio_pipeline);
    audio_pipeline_reset_ringbuffer(g_audio_pipeline);
    audio_pipeline_reset_elements(g_audio_pipeline);
    
    xSemaphoreGive(g_pipeline_mutex);
}

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
        
        // Ferma quando la riproduzione è completata
        if (msg.source_type == AUDIO_ELEMENT_TYPE_ELEMENT 
            && msg.source == (void *) g_i2s_stream_writer
            && msg.cmd == AEL_MSG_CMD_REPORT_STATUS
            && (((int)msg.data == AEL_STATUS_STATE_STOPPED) 
                || ((int)msg.data == AEL_STATUS_STATE_FINISHED))) {
            ESP_LOGI(TAG, "Playback finished");
            stop_audio_pipeline();
        }
    }
}

// Handler HTTP per ricevere e riprodurre audio MP3
static esp_err_t play_audio_handler(httpd_req_t *req)
{
    ESP_LOGI(TAG, "Received audio playback request");
    
    // Ferma eventuale riproduzione in corso
    stop_audio_pipeline();
    vTaskDelay(pdMS_TO_TICKS(500)); // Attendi che la pipeline si fermi
    
    // Leggi l'URL dal corpo della richiesta o dai parametri
    char *url = NULL;
    size_t buf_len = httpd_req_get_url_query_len(req) + 1;
    
    if (buf_len > 1) {
        url = malloc(buf_len);
        if (httpd_req_get_url_query_str(req, url, buf_len) == ESP_OK) {
            ESP_LOGI(TAG, "Found URL query string: %s", url);
            // Estrai l'URL dai parametri query (es: url=http://...)
            char param[256];
            if (httpd_query_key_value(url, "url", param, sizeof(param)) == ESP_OK) {
                free(url);
                url = strdup(param);
            } else {
                // Se non c'è parametro url, usa l'intera query come URL
                // Rimuovi "url=" se presente
                if (strncmp(url, "url=", 4) == 0) {
                    char *temp = url;
                    url = strdup(url + 4);
                    free(temp);
                }
            }
        } else {
            free(url);
            url = NULL;
        }
    }
    
    // Se non c'è URL nei parametri, leggi dal corpo
    if (url == NULL) {
        char content[512];
        int ret = httpd_req_recv(req, content, sizeof(content) - 1);
        if (ret > 0) {
            content[ret] = '\0';
            // Cerca URL nel contenuto (può essere JSON o testo semplice)
            if (strstr(content, "http://") || strstr(content, "https://")) {
                char *url_start = strstr(content, "http");
                char *url_end = strpbrk(url_start, " \n\r\"}");
                if (url_end) {
                    *url_end = '\0';
                    url = strdup(url_start);
                } else {
                    url = strdup(url_start);
                }
            } else {
                // Assume che il contenuto sia direttamente l'URL
                url = strdup(content);
            }
        }
    }
    
    if (url == NULL || strlen(url) == 0) {
        ESP_LOGE(TAG, "No URL provided");
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "URL parameter required");
        return ESP_FAIL;
    }
    
    ESP_LOGI(TAG, "Playing audio from URL: %s", url);
    
    // Prendi il mutex per modificare la pipeline
    xSemaphoreTake(g_pipeline_mutex, portMAX_DELAY);
    
    // Assicurati che il codec sia pronto
    if (g_board_handle && g_board_handle->audio_hal) {
        audio_hal_set_mute(g_board_handle->audio_hal, false);
        // Imposta volume se necessario
        int volume = 70;
        audio_hal_set_volume(g_board_handle->audio_hal, volume);
        ESP_LOGI(TAG, "Codec ready, volume: %d%%, unmuted", volume);
    }
    
    // Configura il nuovo URL
    audio_element_set_uri(g_http_stream_reader, url);
    
    // Breve delay per assicurarsi che tutto sia pronto
    vTaskDelay(pdMS_TO_TICKS(100));
    
    // Avvia la pipeline
    ESP_LOGI(TAG, "Starting audio pipeline...");
    audio_pipeline_run(g_audio_pipeline);
    
    xSemaphoreGive(g_pipeline_mutex);
    
    free(url);
    
    // Rispondi al client
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, "{\"status\":\"playing\",\"message\":\"Audio playback started\"}");
    
    return ESP_OK;
}

// Handler HTTP per ricevere testo e generare URL TTS (per uso futuro con Google TTS API)
static esp_err_t text_handler(httpd_req_t *req)
{
    char content[512];
    int ret = httpd_req_recv(req, content, sizeof(content) - 1);
    
    if (ret <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No text provided");
        return ESP_FAIL;
    }
    
    content[ret] = '\0';
    ESP_LOGI(TAG, "Received text: %s", content);
    
    // Per ora, rispondi che il testo deve essere convertito in audio sul MacBook
    // In futuro, qui si potrebbe chiamare Google TTS API direttamente
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, "{\"status\":\"received\",\"message\":\"Text received. Please send audio URL instead.\"}");
    
    return ESP_OK;
}

// Handler root per informazioni sul server
static esp_err_t root_handler(httpd_req_t *req)
{
    const char *html = 
        "<html><head><title>ESP32 TTS Server</title></head><body>"
        "<h1>ESP32 Text-to-Speech Server</h1>"
        "<p>Endpoints disponibili:</p>"
        "<ul>"
        "<li><b>POST /play</b> - Riproduci audio da URL (body: {\"url\":\"http://...\"} o query: ?url=http://...)</li>"
        "<li><b>POST /text</b> - Invia testo (per uso futuro)</li>"
        "</ul>"
        "</body></html>";
    
    httpd_resp_set_type(req, "text/html");
    httpd_resp_send(req, html, strlen(html));
    return ESP_OK;
}

// Inizializza il server HTTP
static httpd_handle_t start_webserver(void)
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.max_uri_handlers = 10;
    config.lru_purge_enable = true;
    
    httpd_handle_t server = NULL;
    
    if (httpd_start(&server, &config) == ESP_OK) {
        // Handler root
        httpd_uri_t root = {
            .uri = "/",
            .method = HTTP_GET,
            .handler = root_handler,
        };
        httpd_register_uri_handler(server, &root);
        
        // Handler per riprodurre audio
        httpd_uri_t play_uri = {
            .uri = "/play",
            .method = HTTP_POST,
            .handler = play_audio_handler,
        };
        httpd_register_uri_handler(server, &play_uri);
        
        // Handler per ricevere testo
        httpd_uri_t text_uri = {
            .uri = "/text",
            .method = HTTP_POST,
            .handler = text_handler,
        };
        httpd_register_uri_handler(server, &text_uri);
        
        ESP_LOGI(TAG, "HTTP server started on port %d", config.server_port);
    }
    
    return server;
}

void app_main(void)
{
    ESP_LOGI(TAG, "Starting TTS Server...");
    
    // Inizializza NVS
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK(err);
    
    // Inizializza networking
    ESP_ERROR_CHECK(esp_netif_init());
    
    // Crea mutex per pipeline
    g_pipeline_mutex = xSemaphoreCreateMutex();
    
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
        // Fallback: usa l'interfaccia di default
        netif = esp_netif_get_handle_from_ifkey("WIFI_STA_DEF");
        if (netif) {
            esp_netif_get_ip_info(netif, &ip_info);
            ESP_LOGI(TAG, "WiFi connected! IP address: " IPSTR, IP2STR(&ip_info.ip));
        } else {
            ESP_LOGW(TAG, "WiFi connected but could not get IP address");
            memset(&ip_info, 0, sizeof(ip_info));
        }
    }
    
    // Avvia server HTTP
    ESP_LOGI(TAG, "[10] Start HTTP server");
    httpd_handle_t server = start_webserver();
    
    if (server == NULL) {
        ESP_LOGE(TAG, "Failed to start HTTP server");
        return;
    }
    
    if (ip_info.ip.addr != 0) {
        ESP_LOGI(TAG, "TTS Server ready! Send POST requests to http://" IPSTR "/play", IP2STR(&ip_info.ip));
        ESP_LOGI(TAG, "Example: curl -X POST -d '{\"url\":\"http://example.com/audio.mp3\"}' http://" IPSTR "/play", IP2STR(&ip_info.ip));
    } else {
        ESP_LOGI(TAG, "TTS Server ready! Check serial monitor for IP address");
    }
    
    // Loop principale
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

