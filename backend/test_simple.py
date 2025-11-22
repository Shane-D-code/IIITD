import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Device Registration
print("1. Testing device registration...")
response = requests.post(f"{BASE_URL}/api/v1/devices/register")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data["device_token"]
    print(f"✓ Got token: {token[:20]}...")
else:
    print(f"✗ Error: {response.text}")
    exit(1)

# Test 2: Scan endpoint
print("\n2. Testing scan endpoint...")
headers = {"Authorization": f"Bearer {token}"}
payload = {
    "sanitized_text": "URGENT! Click this link to claim your $1000 prize!",
    "urls": ["http://suspicious-site.tk/claim"]
}

response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Risk Score: {data['risk_score']}")
    print(f"✓ Reasons: {data['reasons']}")
    print(f"✓ High Risk Links: {data['high_risk_link_count']}")
else:
    print(f"✗ Error: {response.text}")

# Test 3: Low risk content
print("\n3. Testing low risk content...")
payload_safe = {
    "sanitized_text": "Hello, this is a normal message.",
    "urls": ["https://google.com"]
}

response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload_safe, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"✓ Risk Score: {data['risk_score']}")
    print(f"✓ Reasons: {data['reasons']}")
else:
    print(f"✗ Error: {response.text}")

print("\n✓ All tests completed!")