/* Play mp3 file by audio pipeline
   with possibility to start, stop, pause and resume playback
   as well as adjust volume

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_log.h"
#include "audio_element.h"
#include "audio_pipeline.h"
#include "audio_event_iface.h"
#include "audio_mem.h"
#include "audio_common.h"
#include "i2s_stream.h"
#include "mp3_decoder.h"
#include "fatfs_stream.h"
#include "esp_peripherals.h"
#include "periph_touch.h"
#include "periph_adc_button.h"
#include "periph_button.h"
#include "board.h"
#include "periph_sdcard.h"

static const char *TAG = "PLAY_SD_MP3_CONTROL";

#define SD_MOUNT_POINT "/sdcard"
#define MP3_FILE_PATH "/sdcard/test.mp3"

void app_main(void)
{
    audio_pipeline_handle_t pipeline;
    audio_element_handle_t i2s_stream_writer, mp3_decoder, fatfs_stream_reader;

    esp_log_level_set("*", ESP_LOG_WARN);
    esp_log_level_set(TAG, ESP_LOG_INFO);

    ESP_LOGI(TAG, "[ 1 ] Start audio codec chip");
    audio_board_handle_t board_handle = audio_board_init();
    if (board_handle == NULL) {
        ESP_LOGE(TAG, "Failed to initialize audio board");
        return;
    }
    
    if (board_handle->audio_hal != NULL) {
        audio_hal_ctrl_codec(board_handle->audio_hal, AUDIO_HAL_CODEC_MODE_DECODE, AUDIO_HAL_CTRL_START);
    } else {
        ESP_LOGW(TAG, "Audio HAL is NULL, continuing without hardware codec");
    }

    int player_volume = 60; // Volume di default
    if (board_handle->audio_hal != NULL) {
        audio_hal_get_volume(board_handle->audio_hal, &player_volume);
    }

    ESP_LOGI(TAG, "[ 2 ] Initialize SD card");
    esp_periph_config_t periph_cfg = DEFAULT_ESP_PERIPH_SET_CONFIG();
    esp_periph_set_handle_t set = esp_periph_set_init(&periph_cfg);
    
    ESP_LOGI(TAG, "[2.1] Mount SD card");
    esp_err_t sdcard_ret = audio_board_sdcard_init(set, SD_MODE_SPI); // Modalità SPI (più stabile, evita errori DMA 0x107)
    if (sdcard_ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize SD card: %d", sdcard_ret);
    } else {
        vTaskDelay(pdMS_TO_TICKS(2000));  // Attende 2 secondi per stabilizzare la SD
        
        // Verifica che il file esista
        struct stat file_stat;
        if (stat(MP3_FILE_PATH, &file_stat) == 0) {
            ESP_LOGI(TAG, "[2.3] File %s found, size: %ld bytes", MP3_FILE_PATH, file_stat.st_size);
        } else {
            ESP_LOGE(TAG, "[2.3] File %s NOT FOUND! Please ensure the file exists on the SD card", MP3_FILE_PATH);
            ESP_LOGI(TAG, "[2.4] Listing files in %s:", SD_MOUNT_POINT);
            DIR *dir = opendir(SD_MOUNT_POINT);
            if (dir != NULL) {
                struct dirent *entry;
                while ((entry = readdir(dir)) != NULL) {
                    ESP_LOGI(TAG, "  - %s", entry->d_name);
                }
                closedir(dir);
            } else {
                ESP_LOGE(TAG, "Failed to open directory %s", SD_MOUNT_POINT);
            }
        }
        
        // Delay per assicurarsi che la SD card sia completamente pronta
        ESP_LOGI(TAG, "[2.5] Waiting for SD card to stabilize...");
        vTaskDelay(2000 / portTICK_PERIOD_MS);  // 2 secondi per stabilizzare completamente
        
        // NOTA: I test di lettura sono stati disabilitati perché potrebbero interferire
        // con l'inizializzazione DMA di fatfs_stream. La SD card è già stata verificata
        // durante il montaggio e il controllo dell'esistenza del file.
    }

    ESP_LOGI(TAG, "[ 3 ] Create audio pipeline, add all elements to pipeline, and subscribe pipeline event");
    audio_pipeline_cfg_t pipeline_cfg = DEFAULT_AUDIO_PIPELINE_CONFIG();
    pipeline = audio_pipeline_init(&pipeline_cfg);
    mem_assert(pipeline);

    ESP_LOGI(TAG, "[3.1] Create fatfs stream to read MP3 file from SD card");
    fatfs_stream_cfg_t fatfs_cfg = FATFS_STREAM_CFG_DEFAULT();
    fatfs_cfg.type = AUDIO_STREAM_READER;
    // Buffer grandi per ridurre il numero di letture DMA e minimizzare timeout
    // Buffer più grandi = meno letture DMA = meno probabilità di timeout
    fatfs_cfg.buf_sz = 4096;  // Buffer grande per ridurre letture DMA
    fatfs_cfg.out_rb_size = 16 * 1024;  // Ring buffer molto grande per bufferizzare più dati
    fatfs_stream_reader = fatfs_stream_init(&fatfs_cfg);
    audio_element_set_uri(fatfs_stream_reader, MP3_FILE_PATH);
    
    // Delay molto lungo per assicurarsi che la SD card sia completamente pronta
    // e che il DMA sia completamente inizializzato prima di iniziare la lettura
    ESP_LOGI(TAG, "[3.1.1] Waiting for SD card DMA to stabilize...");
    vTaskDelay(2000 / portTICK_PERIOD_MS);  // Aumentato a 2 secondi per massima stabilità

    ESP_LOGI(TAG, "[3.2] Create mp3 decoder to decode mp3 file");
    mp3_decoder_cfg_t mp3_cfg = DEFAULT_MP3_DECODER_CONFIG();
    mp3_decoder = mp3_decoder_init(&mp3_cfg);

    ESP_LOGI(TAG, "[3.3] Create i2s stream to write data to codec chip");
#if defined CONFIG_ESP32_C3_LYRA_V2_BOARD
    i2s_stream_cfg_t i2s_cfg = I2S_STREAM_PDM_TX_CFG_DEFAULT();
#else
    i2s_stream_cfg_t i2s_cfg = I2S_STREAM_CFG_DEFAULT();
#endif
    i2s_cfg.type = AUDIO_STREAM_WRITER;
    i2s_stream_writer = i2s_stream_init(&i2s_cfg);

    ESP_LOGI(TAG, "[3.4] Register all elements to audio pipeline");
    audio_pipeline_register(pipeline, fatfs_stream_reader, "file");
    audio_pipeline_register(pipeline, mp3_decoder, "mp3");
    audio_pipeline_register(pipeline, i2s_stream_writer, "i2s");

    ESP_LOGI(TAG, "[3.5] Link it together [SD file]-->mp3_decoder-->i2s_stream-->[codec_chip]");
    const char *link_tag[3] = {"file", "mp3", "i2s"};
    audio_pipeline_link(pipeline, &link_tag[0], 3);

    ESP_LOGI(TAG, "[3.6] Initialize keys on board");
    audio_board_key_init(set);

    ESP_LOGI(TAG, "[ 4 ] Set up  event listener");
    audio_event_iface_cfg_t evt_cfg = AUDIO_EVENT_IFACE_DEFAULT_CFG();
    audio_event_iface_handle_t evt = audio_event_iface_init(&evt_cfg);

    ESP_LOGI(TAG, "[4.1] Listening event from all elements of pipeline");
    audio_pipeline_set_listener(pipeline, evt);

    ESP_LOGI(TAG, "[4.2] Listening event from peripherals");
    audio_event_iface_set_listener(esp_periph_set_get_event_iface(set), evt);

    ESP_LOGW(TAG, "[ 5 ] Tap touch buttons to control music player:");
    ESP_LOGW(TAG, "      [Play] to start, pause and resume, [Set] to stop.");
    ESP_LOGW(TAG, "      [Vol-] or [Vol+] to adjust volume.");

    ESP_LOGI(TAG, "[ 5.1 ] Start audio_pipeline");
    ESP_LOGI(TAG, "[ 5.2 ] Playing file: %s", MP3_FILE_PATH);
    audio_pipeline_run(pipeline);

    while (1) {
        audio_event_iface_msg_t msg;
        esp_err_t ret = audio_event_iface_listen(evt, &msg, portMAX_DELAY);
        if (ret != ESP_OK) {
            continue;
        }

        if (msg.source_type == AUDIO_ELEMENT_TYPE_ELEMENT && msg.source == (void *) mp3_decoder
            && msg.cmd == AEL_MSG_CMD_REPORT_MUSIC_INFO) {
            audio_element_info_t music_info = {0};
            audio_element_getinfo(mp3_decoder, &music_info);
            ESP_LOGI(TAG, "[ * ] Receive music info from mp3 decoder, sample_rates=%d, bits=%d, ch=%d",
                     music_info.sample_rates, music_info.bits, music_info.channels);
            i2s_stream_set_clk(i2s_stream_writer, music_info.sample_rates, music_info.bits, music_info.channels);
            continue;
        }

        if ((msg.source_type == PERIPH_ID_TOUCH || msg.source_type == PERIPH_ID_BUTTON || msg.source_type == PERIPH_ID_ADC_BTN)
            && (msg.cmd == PERIPH_TOUCH_TAP || msg.cmd == PERIPH_BUTTON_PRESSED || msg.cmd == PERIPH_ADC_BUTTON_PRESSED)) {
            if ((int) msg.data == get_input_play_id()) {
                ESP_LOGI(TAG, "[ * ] [Play] touch tap event");
                audio_element_state_t el_state = audio_element_get_state(i2s_stream_writer);
                switch (el_state) {
                    case AEL_STATE_INIT :
                        ESP_LOGI(TAG, "[ * ] Starting audio pipeline");
                        audio_pipeline_run(pipeline);
                        break;
                    case AEL_STATE_RUNNING :
                        ESP_LOGI(TAG, "[ * ] Pausing audio pipeline");
                        audio_pipeline_pause(pipeline);
                        break;
                    case AEL_STATE_PAUSED :
                        ESP_LOGI(TAG, "[ * ] Resuming audio pipeline");
                        audio_pipeline_resume(pipeline);
                        break;
                    case AEL_STATE_FINISHED :
                        ESP_LOGI(TAG, "[ * ] Rewinding audio pipeline");
                        audio_pipeline_reset_ringbuffer(pipeline);
                        audio_pipeline_reset_elements(pipeline);
                        audio_pipeline_change_state(pipeline, AEL_STATE_INIT);
                        audio_element_set_uri(fatfs_stream_reader, MP3_FILE_PATH);
                        audio_pipeline_run(pipeline);
                        break;
                    default :
                        ESP_LOGI(TAG, "[ * ] Not supported state %d", el_state);
                }
            } else if ((int) msg.data == get_input_set_id()) {
                ESP_LOGI(TAG, "[ * ] [Set] touch tap event");
                ESP_LOGI(TAG, "[ * ] Stopping audio pipeline");
                break;
            } else if ((int) msg.data == get_input_mode_id()) {
                ESP_LOGI(TAG, "[ * ] [mode] tap event");
                audio_pipeline_stop(pipeline);
                audio_pipeline_wait_for_stop(pipeline);
                audio_pipeline_terminate(pipeline);
                audio_pipeline_reset_ringbuffer(pipeline);
                audio_pipeline_reset_elements(pipeline);
                audio_element_set_uri(fatfs_stream_reader, MP3_FILE_PATH);
                audio_pipeline_run(pipeline);
            } else if ((int) msg.data == get_input_volup_id()) {
                ESP_LOGI(TAG, "[ * ] [Vol+] touch tap event");
                player_volume += 10;
                if (player_volume > 100) {
                    player_volume = 100;
                }
                if (board_handle->audio_hal != NULL) {
                    audio_hal_set_volume(board_handle->audio_hal, player_volume);
                }
                ESP_LOGI(TAG, "[ * ] Volume set to %d %%", player_volume);
            } else if ((int) msg.data == get_input_voldown_id()) {
                ESP_LOGI(TAG, "[ * ] [Vol-] touch tap event");
                player_volume -= 10;
                if (player_volume < 0) {
                    player_volume = 0;
                }
                if (board_handle->audio_hal != NULL) {
                    audio_hal_set_volume(board_handle->audio_hal, player_volume);
                }
                ESP_LOGI(TAG, "[ * ] Volume set to %d %%", player_volume);
            }
        }
    }

    ESP_LOGI(TAG, "[ 6 ] Stop audio_pipeline");
    audio_pipeline_stop(pipeline);
    audio_pipeline_wait_for_stop(pipeline);
    audio_pipeline_terminate(pipeline);
    audio_pipeline_unregister(pipeline, fatfs_stream_reader);
    audio_pipeline_unregister(pipeline, mp3_decoder);
    audio_pipeline_unregister(pipeline, i2s_stream_writer);

    /* Terminate the pipeline before removing the listener */
    audio_pipeline_remove_listener(pipeline);

    /* Make sure audio_pipeline_remove_listener is called before destroying event_iface */
    audio_event_iface_destroy(evt);

    /* Release all resources */
    audio_pipeline_deinit(pipeline);
    audio_element_deinit(fatfs_stream_reader);
    audio_element_deinit(i2s_stream_writer);
    audio_element_deinit(mp3_decoder);
}
