"""
Test script for Flask Webhook API

This script demonstrates how to test the webhook endpoints.
"""

import requests
import json
import time


def test_health_check(base_url):
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_generic_webhook(base_url):
    """Test the generic webhook endpoint"""
    print("\n🔍 Testing generic webhook endpoint...")
    
    test_payload = {
        "event": "test_event",
        "timestamp": int(time.time()),
        "data": {
            "message": "Hello from test script",
            "user_id": 12345,
            "action": "user_login"
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/webhook",
            json=test_payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_github_webhook(base_url):
    """Test the GitHub webhook endpoint"""
    print("\n🔍 Testing GitHub webhook endpoint...")
    
    github_payload = {
        "ref": "refs/heads/main",
        "before": "abc123",
        "after": "def456",
        "repository": {
            "name": "test-repo",
            "full_name": "user/test-repo",
            "owner": {
                "login": "testuser"
            }
        },
        "pusher": {
            "name": "Test User",
            "email": "test@example.com"
        },
        "commits": [
            {
                "id": "def456",
                "message": "Test commit",
                "author": {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/webhook/github",
            json=github_payload,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Event": "push"
            }
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_invalid_json(base_url):
    """Test webhook with invalid JSON"""
    print("\n🔍 Testing invalid JSON handling...")
    
    try:
        response = requests.post(
            f"{base_url}/webhook",
            data="invalid json data",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    base_url = "http://localhost:5000"
    
    print("🚀 Starting Flask Webhook API Tests")
    print(f"Testing against: {base_url}")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    tests = [
        ("Health Check", test_health_check),
        ("Generic Webhook", test_generic_webhook),
        ("GitHub Webhook", test_github_webhook),
        ("Invalid JSON", test_invalid_json)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func(base_url)
        results.append((test_name, result))
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your webhook API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for more details.")


if __name__ == "__main__":
    main()