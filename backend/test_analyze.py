import requests

BASE_URL = "http://localhost:8000"

# Test /analyze endpoint specifically
response = requests.post(f"{BASE_URL}/api/v1/devices/register")
token = response.json()["device_token"]

headers = {"Authorization": f"Bearer {token}"}
payload = {
    "sanitized_text": "URGENT! Your account will be suspended! Click here: http://fake-bank.tk/verify",
    "urls": ["http://fake-bank.tk/verify", "https://suspicious-update.ml/confirm"]
}

response = requests.post(f"{BASE_URL}/api/v1/analyze", json=payload, headers=headers)
print(f"✓ /analyze endpoint works: {response.status_code}")
print(f"✓ Response: {response.json()}")