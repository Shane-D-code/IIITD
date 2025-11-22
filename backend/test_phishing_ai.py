import requests

BASE_URL = "http://localhost:8000"

# Test phishing-specific AI model
response = requests.post(f"{BASE_URL}/api/v1/devices/register")
token = response.json()["device_token"]

headers = {"Authorization": f"Bearer {token}"}

# Test cases for phishing detection
test_cases = [
    {
        "name": "Clear Phishing",
        "text": "URGENT! Your PayPal account has been suspended! Click here to verify immediately or lose access forever!",
        "urls": ["http://paypal-verify.tk/urgent"]
    },
    {
        "name": "Moderate Phishing", 
        "text": "You have won a prize! Click to claim your reward.",
        "urls": ["https://prize-claim.ml/winner"]
    },
    {
        "name": "Legitimate Content",
        "text": "Thank you for your recent purchase. Your order will arrive in 3-5 business days.",
        "urls": ["https://amazon.com/orders"]
    }
]

print("=== Phishing AI Model Test ===")
for test in test_cases:
    payload = {
        "sanitized_text": test["text"],
        "urls": test["urls"]
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
    data = response.json()
    
    print(f"\n{test['name']}:")
    print(f"  Risk Score: {data['risk_score']:.3f}")
    print(f"  Reasons:")
    for reason in data['reasons']:
        print(f"    - {reason}")