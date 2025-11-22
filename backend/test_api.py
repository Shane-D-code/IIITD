import requests
import json
import asyncio
import websockets

BASE_URL = "http://localhost:8000"

def test_device_registration():
    response = requests.post(f"{BASE_URL}/api/v1/devices/register")
    assert response.status_code == 200
    data = response.json()
    assert "device_token" in data
    return data["device_token"]

def test_scan_endpoint(token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "sanitized_text": "URGENT! Click this link to claim your $1000 prize!",
        "urls": ["http://suspicious-site.tk/claim"]
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_score" in data
    assert "reasons" in data
    assert "high_risk_link_count" in data
    assert data["risk_score"] > 0.5  # Should be high risk
    
    print(f"Risk Score: {data['risk_score']}")
    print(f"Reasons: {data['reasons']}")
    print(f"High Risk Links: {data['high_risk_link_count']}")

async def test_websocket(token):
    uri = f"ws://localhost:8000/ws/updates?token={token}"
    async with websockets.connect(uri) as websocket:
        print("WebSocket connected")
        # Keep connection alive for testing
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("Testing device registration...")
    token = test_device_registration()
    print(f"Got token: {token[:20]}...")
    
    print("\nTesting scan endpoint...")
    test_scan_endpoint(token)
    
    print("\nTesting WebSocket...")
    asyncio.run(test_websocket(token))