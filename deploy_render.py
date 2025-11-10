#!/usr/bin/env python3
"""
Script Python per deploy automatico del server Render
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

RENDER_API_BASE = "https://api.render.com/v1"
SERVICE_NAME = "esp32-test-q46k"

def check_files():
    """Verifica che tutti i file necessari esistano"""
    required_files = ["render_server.py", "requirements.txt", "Procfile"]
    missing = []
    
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ File mancanti: {', '.join(missing)}")
        return False
    
    print("✅ Tutti i file necessari presenti")
    return True

def check_render_cli():
    """Verifica se Render CLI è installato"""
    try:
        result = subprocess.run(
            ["render", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Render CLI trovato: {result.stdout.strip()}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("⚠️  Render CLI non trovato")
    return False

def deploy_via_cli():
    """Deploy usando Render CLI"""
    print("\n🚀 Deploy via Render CLI...")
    
    # Verifica login
    try:
        result = subprocess.run(
            ["render", "whoami"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            print("❌ Non sei loggato in Render CLI")
            print("   Esegui: render login")
            return False
        print(f"✅ Loggato come: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Errore verifica login: {e}")
        return False
    
    # Crea o aggiorna servizio
    print(f"\n📦 Deploy servizio: {SERVICE_NAME}")
    
    # Verifica se il servizio esiste
    try:
        result = subprocess.run(
            ["render", "services", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        service_exists = SERVICE_NAME in result.stdout
    except Exception as e:
        print(f"⚠️  Errore verifica servizio: {e}")
        service_exists = False
    
    if not service_exists:
        print("📝 Creazione nuovo servizio...")
        try:
            subprocess.run(
                [
                    "render", "services", "create", "web",
                    "--name", SERVICE_NAME,
                    "--env", "python",
                    "--buildCommand", "pip install -r requirements.txt",
                    "--startCommand", "gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120",
                    "--region", "oregon",
                    "--plan", "free"
                ],
                check=True,
                timeout=30
            )
            print("✅ Servizio creato")
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore creazione servizio: {e}")
            return False
    else:
        print("✅ Servizio già esistente")
        print("   Per aggiornare, usa: render services deploy")
    
    print(f"\n✅ Deploy completato!")
    print(f"🌐 URL: https://{SERVICE_NAME}.onrender.com")
    return True

def deploy_via_github():
    """Istruzioni per deploy via GitHub"""
    print("\n📋 Deploy Manuale via GitHub:")
    print("=" * 50)
    print("1. Crea un repository GitHub (se non esiste)")
    print("2. Aggiungi questi file al repository:")
    print("   - render_server.py")
    print("   - requirements.txt")
    print("   - Procfile")
    print("3. Vai su https://dashboard.render.com")
    print("4. Crea nuovo 'Web Service'")
    print("5. Collega il repository GitHub")
    print("6. Configurazione:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120")
    print("   - Plan: Free")
    print("7. Deploy!")
    print("=" * 50)

def deploy_via_manual_upload():
    """Istruzioni per deploy manuale"""
    print("\n📋 Deploy Manuale (Upload File):")
    print("=" * 50)
    print("1. Vai su https://dashboard.render.com")
    print("2. Crea nuovo 'Web Service'")
    print("3. Nome servizio: esp32-test-q46k")
    print("4. Environment: Python 3")
    print("5. Build Command: pip install -r requirements.txt")
    print("6. Start Command: gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120")
    print("7. Carica i file:")
    print("   - render_server.py")
    print("   - requirements.txt")
    print("   - Procfile")
    print("8. Deploy!")
    print("=" * 50)

def main():
    print("🚀 Deploy Server Render")
    print("=" * 50)
    print()
    
    # Verifica file
    if not check_files():
        sys.exit(1)
    
    # Prova deploy via CLI
    if check_render_cli():
        if deploy_via_cli():
            print("\n✅ Deploy completato con successo!")
            print(f"🌐 URL: https://{SERVICE_NAME}.onrender.com")
            print("\n📊 Monitora i log:")
            print(f"   render services logs {SERVICE_NAME}")
            return
    
    # Fallback: istruzioni manuali
    print("\n⚠️  Deploy automatico non disponibile")
    print("   Usa una delle opzioni manuali:\n")
    
    deploy_via_github()
    print()
    deploy_via_manual_upload()
    
    print("\n💡 Suggerimento:")
    print("   Installa Render CLI per deploy automatico:")
    print("   brew install render")
    print("   render login")

if __name__ == "__main__":
    main()

