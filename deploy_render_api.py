#!/usr/bin/env python3
"""
Deploy automatico su Render usando l'API
Richiede RENDER_API_KEY come variabile d'ambiente
"""

import os
import sys
import requests
import json
from pathlib import Path

RENDER_API_BASE = "https://api.render.com/v1"
SERVICE_NAME = "esp32-test-q46k"

def get_api_key():
    """Ottieni API key da variabile d'ambiente"""
    api_key = os.environ.get("RENDER_API_KEY")
    if not api_key:
        print("❌ RENDER_API_KEY non trovata")
        print("\nPer ottenere l'API key:")
        print("1. Vai su https://dashboard.render.com/account/api-keys")
        print("2. Crea una nuova API key")
        print("3. Esegui: export RENDER_API_KEY='tua-api-key'")
        print("4. Oppure: RENDER_API_KEY='tua-api-key' python3 deploy_render_api.py")
        return None
    return api_key

def get_headers(api_key):
    """Crea headers per richieste API"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def check_service_exists(api_key):
    """Verifica se il servizio esiste già"""
    headers = get_headers(api_key)
    
    try:
        response = requests.get(
            f"{RENDER_API_BASE}/services",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        services = response.json()
        for service in services:
            if service.get("name") == SERVICE_NAME:
                return service.get("id")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore verifica servizio: {e}")
        return None

def create_service(api_key, owner_id):
    """Crea nuovo servizio su Render"""
    headers = get_headers(api_key)
    
    service_data = {
        "type": "web_service",
        "name": SERVICE_NAME,
        "ownerId": owner_id,
        "repo": None,  # Manual deploy
        "env": "python",
        "region": "oregon",
        "planId": "free",
        "branch": "main",
        "rootDir": "/",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120",
        "autoDeploy": "yes"
    }
    
    try:
        response = requests.post(
            f"{RENDER_API_BASE}/services",
            headers=headers,
            json=service_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore creazione servizio: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return None

def get_owner_id(api_key):
    """Ottieni owner ID (user ID)"""
    headers = get_headers(api_key)
    
    try:
        response = requests.get(
            f"{RENDER_API_BASE}/owners",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        owners = response.json()
        if owners:
            return owners[0].get("id")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore ottenimento owner ID: {e}")
        return None

def upload_files(api_key, service_id):
    """Carica file al servizio (richiede repository Git)"""
    print("⚠️  Upload file richiede repository Git")
    print("   Per deploy manuale, usa il dashboard Render")
    return False

def main():
    print("🚀 Deploy Server Render via API")
    print("=" * 50)
    print()
    
    # Verifica file
    required_files = ["render_server.py", "requirements.txt", "Procfile"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ File mancante: {file}")
            sys.exit(1)
    print("✅ Tutti i file presenti")
    print()
    
    # Ottieni API key
    api_key = get_api_key()
    if not api_key:
        sys.exit(1)
    
    print("✅ API key trovata")
    print()
    
    # Verifica se servizio esiste
    print(f"🔍 Verifica servizio: {SERVICE_NAME}")
    service_id = check_service_exists(api_key)
    
    if service_id:
        print(f"✅ Servizio già esistente (ID: {service_id})")
        print(f"🌐 URL: https://{SERVICE_NAME}.onrender.com")
        print("\n💡 Per aggiornare, usa il dashboard Render o Render CLI")
        return
    
    print("📝 Servizio non trovato, creazione nuovo servizio...")
    print()
    
    # Ottieni owner ID
    print("🔍 Ottenimento owner ID...")
    owner_id = get_owner_id(api_key)
    if not owner_id:
        print("❌ Impossibile ottenere owner ID")
        sys.exit(1)
    print(f"✅ Owner ID: {owner_id}")
    print()
    
    # Crea servizio
    print("📦 Creazione servizio...")
    service = create_service(api_key, owner_id)
    
    if service:
        print("✅ Servizio creato con successo!")
        print()
        print(f"🌐 URL: https://{SERVICE_NAME}.onrender.com")
        print(f"📊 ID Servizio: {service.get('id')}")
        print()
        print("⚠️  NOTA: Per deploy manuale, devi ancora:")
        print("   1. Caricare i file via dashboard Render")
        print("   2. Oppure collegare un repository Git")
        print()
        print("💡 Suggerimento: Usa GitHub per deploy automatico")
    else:
        print("❌ Errore creazione servizio")
        print("\n💡 Prova il deploy manuale:")
        print("   1. Vai su https://dashboard.render.com")
        print("   2. Crea nuovo Web Service")
        print("   3. Segui le istruzioni in DEPLOY_ISTRUZIONI.md")
        sys.exit(1)

if __name__ == "__main__":
    main()

