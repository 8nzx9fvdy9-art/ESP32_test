# 🐍 Installazione Dipendenze Python

## ✅ Ambiente Virtuale Creato!

Ho già creato un **ambiente virtuale Python** per il progetto e installato `websockets`.

## 🚀 Come Usare l'Ambiente Virtuale

### Attivare l'Ambiente Virtuale

**Ogni volta** che apri un **NUOVO terminale** per eseguire il server o il client Python, devi attivare l'ambiente virtuale:

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
```

✅ **Quando l'ambiente è attivo**, vedrai `(venv)` all'inizio della riga del terminale:

```bash
(venv) edoardocolella@MacCole ESP32_test %
```

### Eseguire il Server Python

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 server_websocket.py
```

### Eseguire il Client MacBook

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_client.py
```

## 📝 Workflow Completo

### Terminale Mac 1 - Server Python:
```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 server_websocket.py
```

### Terminale Mac 2 - ngrok:
```bash
ngrok http 8765
```

### Terminale Mac 3 - Client MacBook:
```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 macbook_client.py
```

## ⚠️ Note Importanti

- **Ogni nuovo terminale**: Devi attivare l'ambiente virtuale con `source venv/bin/activate`
- **Quando vedi `(venv)`**: L'ambiente è attivo e puoi eseguire i comandi Python
- **Se dimentichi di attivare**: Vedrai l'errore `ModuleNotFoundError: No module named 'websockets'`

## 🆘 Problemi?

### Errore: `ModuleNotFoundError: No module named 'websockets'`

**Soluzione**: Attiva l'ambiente virtuale prima di eseguire il comando:

```bash
source venv/bin/activate
```

### Come verificare che l'ambiente sia attivo

Dovresti vedere `(venv)` all'inizio della riga del terminale:

```bash
(venv) edoardocolella@MacCole ESP32_test %
```

Se **NON** vedi `(venv)`, l'ambiente non è attivo. Esegui:

```bash
source venv/bin/activate
```

