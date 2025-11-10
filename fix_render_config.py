#!/usr/bin/env python3
"""
Script per aggiornare la configurazione Render via API
Richiede RENDER_API_KEY come variabile d'ambiente
"""

import os
import sys
import requests
import json

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
        print("4. Oppure: RENDER_API_KEY='tua-api-key' python3 fix_render_config.py")
        return None
    return api_key

def get_headers(api_key):
    """Crea headers per richieste API"""
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def find_service(api_key):
    """Trova il servizio per nome"""
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
            if service.get("name") == SERVICE_NAME or "esp32" in service.get("name", "").lower():
                return service
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore ricerca servizio: {e}")
        return None

def update_service_config(api_key, service_id):
    """Aggiorna la configurazione del servizio"""
    headers = get_headers(api_key)
    
    # Aggiorna solo lo start command
    update_data = {
        "startCommand": "gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120"
    }
    
    try:
        response = requests.patch(
            f"{RENDER_API_BASE}/services/{service_id}",
            headers=headers,
            json=update_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore aggiornamento servizio: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return None

def main():
    print("🔧 Fix Configurazione Render")
    print("=" * 50)
    print()
    
    # Ottieni API key
    api_key = get_api_key()
    if not api_key:
        print("\n💡 Alternativa: Aggiorna manualmente nel dashboard Render")
        print("   1. Vai su https://dashboard.render.com")
        print("   2. Apri il servizio")
        print("   3. Vai a Settings > Start Command")
        print("   4. Cambia in: gunicorn render_server:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120")
        print("   5. Salva e fai Manual Deploy")
        sys.exit(1)
    
    print("✅ API key trovata")
    print()
    
    # Trova servizio
    print(f"🔍 Ricerca servizio: {SERVICE_NAME}")
    service = find_service(api_key)
    
    if not service:
        print(f"❌ Servizio '{SERVICE_NAME}' non trovato")
        print("\n💡 Verifica il nome del servizio nel dashboard Render")
        sys.exit(1)
    
    service_id = service.get("id")
    service_name = service.get("name")
    print(f"✅ Servizio trovato: {service_name} (ID: {service_id})")
    print()
    
    # Aggiorna configurazione
    print("📝 Aggiornamento configurazione...")
    updated_service = update_service_config(api_key, service_id)
    
    if updated_service:
        print("✅ Configurazione aggiornata con successo!")
        print()
        print(f"🌐 URL: https://{service_name}.onrender.com")
        print()
        print("💡 Ora fai Manual Deploy dal dashboard Render")
        print("   oppure attendi il prossimo deploy automatico")
    else:
        print("❌ Errore aggiornamento configurazione")
        print("\n💡 Aggiorna manualmente nel dashboard Render")

if __name__ == "__main__":
    main()

