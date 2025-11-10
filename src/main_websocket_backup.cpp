#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>

// ===== CONFIGURAZIONE WIFI =====
// Modifica questi valori con le credenziali della tua rete WiFi
const char* ssid = "2-WifiCole";
const char* password = "Nr8w1n46zp3b?";

// ===== CONFIGURAZIONE SERVER =====
// Indirizzo del server WebSocket su Render.com
const char* websocket_server = "esp32-test-q46k.onrender.com";  // Server Render
const int websocket_port = 443;
const char* websocket_path = "/";

WebSocketsClient webSocket;

// Buffer per messaggi in arrivo
String lastMessage = "";

// Flag per indicare se siamo connessi
bool wsConnected = false;

// Funzione chiamata quando si riceve un messaggio dal server
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("[WebSocket] Disconnesso");
            wsConnected = false;
            break;
            
        case WStype_CONNECTED:
            Serial.print("[WebSocket] Connesso a: ");
            Serial.println((char*)payload);
            wsConnected = true;
            // Invia un messaggio di benvenuto
            webSocket.sendTXT("ESP32 connesso!");
            break;
            
        case WStype_TEXT: {
            // Messaggio ricevuto dal server (o dal MacBook tramite server)
            lastMessage = String((char*)payload);
            Serial.print("[WebSocket] Messaggio ricevuto: ");
            Serial.println(lastMessage);
            
            // Esempio: rispondi al messaggio
            String response = "ESP32 ha ricevuto: " + lastMessage;
            webSocket.sendTXT(response);
            break;
        }
            
        case WStype_BIN:
            Serial.print("[WebSocket] Dati binari ricevuti, lunghezza: ");
            Serial.println(length);
            break;
            
        case WStype_ERROR:
            Serial.print("[WebSocket] Errore: ");
            if (payload != NULL && length > 0) {
                Serial.println((char*)payload);
            } else {
                Serial.print("Codice errore: ");
                Serial.println(length);
            }
            break;
            
        default:
            break;
    }
}

// Funzione per inviare un messaggio al MacBook (tramite server)
void sendMessageToMacBook(const String& message) {
    if (wsConnected) {
        // Crea una copia non-const perché sendTXT richiede String&
        String msg = message;
        webSocket.sendTXT(msg);
        Serial.print("[WebSocket] Messaggio inviato: ");
        Serial.println(message);
    } else {
        Serial.println("[WebSocket] Non connesso, impossibile inviare messaggio");
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println();
    Serial.println("ESP32 WebSocket Client - Comunicazione Full-Duplex");
    Serial.println("================================================");
    
    // Connessione WiFi
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    Serial.print("Connessione a WiFi: ");
    Serial.println(ssid);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.println("WiFi connesso!");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println();
        Serial.println("Errore: impossibile connettersi al WiFi");
        Serial.println("Verifica SSID e password in main.cpp");
        for(;;) delay(1000);
    }
    
    // Configurazione WebSocket
    // Per HTTPS/WSS (Render.com), usa beginSSL per connessione sicura
    if (websocket_port == 443) {
        // Connessione sicura (WSS) per Render HTTPS
        // beginSSL accetta certificati SSL validi (Render usa certificati validi)
        webSocket.beginSSL(websocket_server, websocket_port, websocket_path);
    } else {
        // Connessione normale (WS) per HTTP
        webSocket.begin(websocket_server, websocket_port, websocket_path);
    }
    webSocket.onEvent(webSocketEvent);
    webSocket.setReconnectInterval(5000);  // Riconnessione automatica ogni 5 secondi
    
    Serial.print("Tentativo di connessione a WebSocket server: ");
    Serial.print(websocket_server);
    Serial.print(":");
    Serial.println(websocket_port);
}

void loop() {
    // Mantieni la connessione WebSocket attiva
    webSocket.loop();
    
    // Esempio: invia un messaggio ogni 10 secondi
    static unsigned long lastSend = 0;
    if (wsConnected && (millis() - lastSend > 10000)) {
        String message = "Messaggio da ESP32 - " + String(millis());
        sendMessageToMacBook(message);
        lastSend = millis();
    }
    
    // Esempio: leggi dalla seriale e invia al MacBook
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        if (input.length() > 0) {
            sendMessageToMacBook("ESP32 dice: " + input);
        }
    }
    
    delay(10);
}

