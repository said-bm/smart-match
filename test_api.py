"""
Simple test script for the Product Facet Parser API
Run this after starting the API server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("Testing Health Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_parse_query():
    """Test parse query endpoint"""
    print("\n" + "="*50)
    print("Testing Parse Query Endpoint")
    print("="*50)
    
    test_queries = [
        "Looking for iPhone 13 with 256GB in blue under $800",
        "Samsung Galaxy S21 5G with dual sim",
        "Gaming laptop with RTX 3060 under $1500",
        "Espresso coffee machine with energy class A++",
        "PS5 games rated 18+ in action genre"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = requests.post(
            f"{BASE_URL}/parse",
            json={"query": query, "include_metadata": True}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success!")
            print(f"Facets found: {result.get('facet_count', 0)}")
            print(f"Categories: {result.get('categories_detected', [])}")
            print(f"Facets: {json.dumps(result.get('facets', {}), indent=2)}")
        else:
            print(f"✗ Failed with status {response.status_code}")
            print(f"Error: {response.text}")
        
        print("-" * 50)

def test_schema():
    """Test schema endpoint"""
    print("\n" + "="*50)
    print("Testing Schema Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/facets/categories")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Available categories: {list(result.get('categories', {}).keys())}")
    else:
        print(f"Failed: {response.text}")

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("Product Facet Parser API - Test Suite")
    print("="*50)
    
    try:
        # Test health
        if not test_health():
            print("\n❌ Health check failed. Is the API running?")
            print("Start the API with: python api.py")
            return
        
        # Test schema
        test_schema()
        
        # Test parsing
        test_parse_query()
        
        print("\n" + "="*50)
        print("✓ All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API")
        print("Make sure the API is running: python api.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

