import requests
import torch

# Check GPU before request
print("=== Before API Call ===")
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.1f} MB")

# Make API request
BASE_URL = "http://localhost:8000"
response = requests.post(f"{BASE_URL}/api/v1/devices/register")
token = response.json()["device_token"]

headers = {"Authorization": f"Bearer {token}"}
payload = {
    "sanitized_text": "URGENT! Your account will be suspended! Click now!",
    "urls": ["http://fake-bank.tk/urgent"]
}

print("\n=== Making API Request ===")
response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
data = response.json()

print(f"Response: {data}")

# Check GPU after request
print("\n=== After API Call ===")
if torch.cuda.is_available():
    print(f"GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.1f} MB")