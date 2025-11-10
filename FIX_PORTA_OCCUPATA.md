# 🔧 Fix: Porta 8765 già in uso

## Problema
```
OSError: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8765): [errno 48] address already in use
```

Questo significa che c'è già un'istanza del server Python in esecuzione sulla porta 8765.

## Soluzione

### Opzione 1: Termina il processo esistente (Raccomandato)

**🖥️ Terminale del Mac:**

```bash
# Trova il processo che usa la porta 8765
lsof -i :8765

# Termina il processo (sostituisci PID con il numero che vedi)
kill PID
```

**Esempio:**
```bash
lsof -i :8765
# Output: Python  71279 edoardocolella ...

kill 71279
```

### Opzione 2: Usa una porta diversa

Se preferisci usare una porta diversa, modifica `server_websocket.py`:

```python
port = 8766  # Cambia da 8765 a 8766 (o un'altra porta)
```

E aggiorna anche ngrok:
```bash
ngrok http 8766  # Usa la nuova porta
```

## ✅ Dopo aver risolto

Riavvia il server Python:

```bash
cd /Users/edoardocolella/ESP32_test
source venv/bin/activate
python3 server_websocket.py
```

Dovresti vedere:
```
Server in ascolto su ws://0.0.0.0:8765
```

Senza errori!

