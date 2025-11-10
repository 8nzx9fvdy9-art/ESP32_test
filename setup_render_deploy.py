#!/usr/bin/env python3
"""
Script per configurare il deploy automatico su Render usando il repository GitHub
"""

import webbrowser
import sys

REPO_URL = "https://github.com/8nzx9fvdy9-art/ESP32_test.git"
SERVICE_NAME = "esp32-test-q46k"

def main():
    print("🚀 Setup Deploy Render da GitHub")
    print("=" * 50)
    print()
    print(f"📦 Repository: {REPO_URL}")
    print(f"🌐 Servizio: {SERVICE_NAME}")
    print()
    print("📋 Istruzioni per deploy su Render:")
    print("=" * 50)
    print()
    print("1. Vai su: https://dashboard.render.com")
    print("2. Clicca 'New +' > 'Web Service'")
    print("3. Collega repository GitHub:")
    print(f"   - Repository: {REPO_URL}")
    print("   - Branch: main")
    print()
    print("4. Configurazione:")
    print("   - Name: esp32-test-q46k")
    print("   - Environment: Python 3")
    print("   - Region: Oregon (o più vicino)")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120")
    print("   - Plan: Free")
    print()
    print("5. Clicca 'Create Web Service'")
    print()
    print("6. Attendi il deploy (2-5 minuti)")
    print()
    print("7. Verifica:")
    print(f"   curl https://{SERVICE_NAME}.onrender.com/status")
    print()
    print("=" * 50)
    print()
    
    # Apri il dashboard Render nel browser
    response = input("Vuoi aprire il dashboard Render nel browser? (s/n): ")
    if response.lower() in ['s', 'si', 'y', 'yes']:
        print("🌐 Apertura dashboard Render...")
        webbrowser.open("https://dashboard.render.com")
        print("✅ Dashboard aperto nel browser")
    else:
        print("💡 Vai manualmente su: https://dashboard.render.com")
    
    print()
    print("✅ Setup completato!")
    print(f"🌐 Dopo il deploy, l'URL sarà: https://{SERVICE_NAME}.onrender.com")

if __name__ == "__main__":
    main()

