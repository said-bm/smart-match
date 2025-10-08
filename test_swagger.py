#!/usr/bin/env python3
"""
Quick test script to verify Swagger UI is accessible
"""
import sys
import time
import subprocess
import requests
from multiprocessing import Process

def start_server():
    """Start the API server"""
    subprocess.run(["poetry", "run", "python", "api.py"], check=False)

def test_endpoints():
    """Test that all documentation endpoints are accessible"""
    base_url = "http://localhost:8000"
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    endpoints_to_test = {
        "/docs": "Swagger UI",
        "/redoc": "ReDoc UI",
        "/openapi.json": "OpenAPI Schema"
    }
    
    all_passed = True
    
    for endpoint, name in endpoints_to_test.items():
        try:
            url = f"{base_url}{endpoint}"
            print(f"\nTesting {name} at {url}...")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {name} is accessible (Status: {response.status_code})")
                if endpoint == "/openapi.json":
                    # Verify it's valid JSON
                    data = response.json()
                    print(f"   - OpenAPI version: {data.get('openapi', 'unknown')}")
                    print(f"   - API title: {data.get('info', {}).get('title', 'unknown')}")
                    print(f"   - Number of paths: {len(data.get('paths', {}))}")
            else:
                print(f"❌ {name} returned status {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {name} is not accessible: {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Swagger UI and API Documentation")
    print("=" * 60)
    
    # Start server in background
    server_process = Process(target=start_server)
    server_process.start()
    
    try:
        # Test endpoints
        if test_endpoints():
            print("\n" + "=" * 60)
            print("✅ All documentation endpoints are working!")
            print("=" * 60)
            print("\nYou can access:")
            print("  - Swagger UI: http://localhost:8000/docs")
            print("  - ReDoc:      http://localhost:8000/redoc")
            print("  - OpenAPI:    http://localhost:8000/openapi.json")
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("❌ Some endpoints failed!")
            print("=" * 60)
            sys.exit(1)
    finally:
        # Clean up
        print("\nStopping server...")
        server_process.terminate()
        server_process.join(timeout=2)
        if server_process.is_alive():
            server_process.kill()

