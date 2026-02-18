import requests
import json

try:
    # 1. Check Swagger UI HTML
    print("Checking /docs...")
    resp_docs = requests.get("http://localhost:8000/docs")
    print(f"Status: {resp_docs.status_code}")
    
    # 2. Check OpenAPI Schema
    print("\nChecking /openapi.json...")
    resp_schema = requests.get("http://localhost:8000/openapi.json")
    print(f"Status: {resp_schema.status_code}")
    
    if resp_schema.status_code == 200:
        schema = resp_schema.json()
        print("\nOpenAPI Schema Details:")
        print(f"Title: {schema.get('info', {}).get('title')}")
        print(f"Version: {schema.get('info', {}).get('version')}")
        
        # Check for 'servers' config which might override URL
        servers = schema.get('servers')
        if servers:
            print(f"Servers Configured: {json.dumps(servers, indent=2)}")
        else:
            print("No hardcoded 'servers' in schema (Default behavior: Relative URLs).")
            
except Exception as e:
    print(f"Error checking Swagger UI: {e}")
