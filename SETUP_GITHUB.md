# 🔧 Setup GitHub per Render

## Problema
Il remote GitHub è configurato con `TUO_USERNAME` (placeholder). Devi sostituirlo con il tuo username GitHub reale.

## Soluzione

### Opzione 1: Hai già un repository GitHub

Se hai già creato un repository GitHub:

1. **Ottieni l'URL del tuo repository** (es. `https://github.com/tuo-username/ESP32_test.git`)

2. **Aggiorna il remote:**
   ```bash
   cd /Users/edoardocolella/ESP32_test
   git remote set-url origin https://github.com/TUO_USERNAME_GITHUB/ESP32_test.git
   ```
   (Sostituisci `TUO_USERNAME_GITHUB` con il tuo username GitHub reale)

3. **Fai push:**
   ```bash
   git push -u origin main
   ```

### Opzione 2: Crea un nuovo repository GitHub

1. **Vai su GitHub:**
   - Apri https://github.com
   - Clicca "New repository" (o "+" > "New repository")

2. **Crea il repository:**
   - **Repository name**: `ESP32_test` (o qualsiasi nome)
   - **Visibility**: Public o Private (come preferisci)
   - **NON** selezionare "Initialize this repository with a README"
   - Clicca "Create repository"

3. **Copia l'URL del repository** (es. `https://github.com/tuo-username/ESP32_test.git`)

4. **Aggiorna il remote:**
   ```bash
   cd /Users/edoardocolella/ESP32_test
   git remote set-url origin https://github.com/TUO_USERNAME_GITHUB/ESP32_test.git
   ```
   (Sostituisci `TUO_USERNAME_GITHUB` con il tuo username GitHub reale)

5. **Fai push:**
   ```bash
   git push -u origin main
   ```

### Opzione 3: Usa Render senza GitHub

Render supporta anche deploy da repository Git locale o da ZIP. Ma è più semplice con GitHub.

---

## 📝 Comandi Completi

Dopo aver configurato il remote corretto:

```bash
cd /Users/edoardocolella/ESP32_test

# Verifica che tutti i file siano committati
git status

# Se ci sono file non committati, aggiungili
git add .

# Fai commit (se necessario)
git commit -m "Setup WebSocket server for Render"

# Fai push
git push -u origin main
```

---

## 🎯 Dopo il Push su GitHub

1. Vai su https://render.com
2. Crea nuovo Web Service
3. Connetti il repository GitHub
4. Render farà il deploy automatico
5. Ottieni l'URL (es. `https://websocket-server.onrender.com`)
6. Aggiorna ESP32 e MacBook con l'URL Render

