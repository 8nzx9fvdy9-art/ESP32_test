# 🚀 Push su GitHub - Guida Rapida

## Problema
Git richiede autenticazione per fare il push su GitHub.

## Soluzione: Token di Accesso Personale

### Passo 1: Crea un Token GitHub

1. **Vai su GitHub:**
   - Apri https://github.com/settings/tokens
   - Oppure: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Crea nuovo token:**
   - Clicca "Generate new token" → "Generate new token (classic)"
   - **Note**: `ESP32_test` (o qualsiasi nome)
   - **Expiration**: Scegli (es. 90 giorni o No expiration)
   - **Scopes**: Seleziona almeno `repo` (per accedere ai repository)
   - Clicca "Generate token"

3. **COPIA IL TOKEN** (lo vedrai solo una volta!)
   - Esempio: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Passo 2: Usa il Token per il Push

**Opzione A: Usa il token direttamente nel comando**

```bash
cd /Users/edoardocolella/ESP32_test
git push -u origin main
```

Quando richiesto:
- **Username**: `8nzx9fvdy9-art`
- **Password**: Incolla il token (non la password GitHub!)

**Opzione B: Salva il token in Git (più comodo)**

```bash
cd /Users/edoardocolella/ESP32_test

# Salva il token (sostituisci TOKEN con il tuo token)
git config --global credential.helper store
git push -u origin main
```

Quando richiesto:
- **Username**: `8nzx9fvdy9-art`
- **Password**: Incolla il token

Git salverà le credenziali per i prossimi push.

---

## 🔐 Alternativa: Usa SSH (più sicuro)

Se preferisci usare SSH invece di HTTPS:

1. **Genera chiave SSH** (se non l'hai già):
   ```bash
   ssh-keygen -t ed25519 -C "tua-email@example.com"
   ```

2. **Aggiungi la chiave a GitHub:**
   - Copia la chiave pubblica: `cat ~/.ssh/id_ed25519.pub`
   - Vai su https://github.com/settings/keys
   - Clicca "New SSH key"
   - Incolla la chiave

3. **Cambia remote a SSH:**
   ```bash
   cd /Users/edoardocolella/ESP32_test
   git remote set-url origin git@github.com:8nzx9fvdy9-art/ESP32_test.git
   git push -u origin main
   ```

---

## ✅ Dopo il Push Riuscito

1. Verifica su GitHub: https://github.com/8nzx9fvdy9-art/ESP32_test
2. Dovresti vedere tutti i file del progetto

## 🎯 Prossimi Passi

Dopo il push su GitHub, puoi:
1. Deploy su Render.com (vedi `SOLUZIONE_RENDER.md`)
2. Oppure continuare con ngrok (vedi `SOLUZIONE_RAPIDA.md`)

