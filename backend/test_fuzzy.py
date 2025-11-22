import requests

BASE_URL = "http://localhost:8000"

# Test fuzzy logic integration
response = requests.post(f"{BASE_URL}/api/v1/devices/register")
token = response.json()["device_token"]

headers = {"Authorization": f"Bearer {token}"}

# Test case with multiple risk factors
payload = {
    "sanitized_text": "URGENT! Your account expires today! Click to claim your $5000 prize!",
    "urls": ["http://fake-secure-bank.tk/urgent-verify"]
}

response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
data = response.json()

print("=== Fuzzy Logic Test ===")
print(f"Risk Score: {data['risk_score']}")
print("Reasons:")
for reason in data['reasons']:
    print(f"  - {reason}")
print(f"High Risk Links: {data['high_risk_link_count']}")

# Test low risk case
payload_low = {
    "sanitized_text": "Hello, this is a normal message from your bank.",
    "urls": ["https://legitimate-bank.com/info"]
}

response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload_low, headers=headers)
data_low = response.json()

print("\n=== Low Risk Test ===")
print(f"Risk Score: {data_low['risk_score']}")
print(f"Reasons: {data_low['reasons']}")