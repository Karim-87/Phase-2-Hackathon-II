import requests
import json

# Test signup endpoint
BASE_URL = "http://localhost:8000/api/v1"

# Test data
signup_data = {
    "email": "test@example.com",
    "password": "shortpass123",
    "name": "Test User"
}

try:
    print("Testing signup endpoint...")
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 or response.status_code == 201:
        print("\nSignup successful!")
    else:
        print(f"\nSignup failed with status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("Could not connect to the backend. Is it running on http://localhost:8000?")
except Exception as e:
    print(f"An error occurred: {str(e)}")