# 🔧 Aggiorna Configurazione Render

## ⚠️ Problema

Render sta ancora eseguendo `python3 server_render.py` invece di usare il `Procfile`.

## ✅ Soluzione Rapida (2 minuti)

### Opzione 1: Dashboard Render (PIÙ VELOCE)

1. **Vai su**: https://dashboard.render.com
2. **Apri il servizio** `esp32-test-q46k` (o quello che vedi nella lista)
3. **Clicca su "Settings"** nel menu laterale
4. **Trova "Start Command"** e **cancella tutto** (lascia vuoto)
5. **Clicca "Save Changes"**
6. **Vai su "Manual Deploy"** > **"Deploy latest commit"**

Render userà automaticamente il `Procfile` che contiene:
```
gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
```

### Opzione 2: Aggiorna Start Command

1. **Vai su**: https://dashboard.render.com
2. **Apri il servizio**
3. **Settings** > **"Start Command"**
4. **Cambia in**:
   ```
   gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
   ```
5. **Salva** e fai **Manual Deploy**

### Opzione 3: Via API (se hai API key)

```bash
export RENDER_API_KEY='tua-api-key'
python3 fix_render_config.py
```

---

## ✅ Verifica

Dopo il deploy:

```bash
curl https://esp32-test-q46k.onrender.com/status
```

Dovresti vedere:
```json
{"status": "online", "buffer_size": 0, ...}
```

---

## 📝 Note

- Il `Procfile` è già corretto nel repository
- Render ha una configurazione nel dashboard che sovrascrive il `Procfile`
- Dopo aver aggiornato il dashboard, Render userà il comando corretto

