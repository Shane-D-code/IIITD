import asyncio
import websockets
import json
import requests
import threading
import time

BASE_URL = "http://localhost:8000"

async def test_websocket():
    # Get token first
    response = requests.post(f"{BASE_URL}/api/v1/devices/register")
    token = response.json()["device_token"]
    print(f"Got token: {token[:20]}...")
    
    # Connect WebSocket
    uri = f"ws://localhost:8000/ws/updates?token={token}"
    
    async with websockets.connect(uri) as websocket:
        print("✓ WebSocket connected")
        
        # Send scan request in background
        def send_scan():
            time.sleep(0.5)  # Small delay
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "sanitized_text": "URGENT! Act now!",
                "urls": ["http://bad-site.tk"]
            }
            requests.post(f"{BASE_URL}/api/v1/scan", json=payload, headers=headers)
        
        # Start scan in background
        threading.Thread(target=send_scan).start()
        
        # Wait for WebSocket message
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            data = json.loads(message)
            print(f"✓ WebSocket message received: {data}")
            print(f"✓ Score: {data['score']}")
            print(f"✓ High risk links: {data['high_risk_link_count']}")
        except asyncio.TimeoutError:
            print("✗ No WebSocket message received")

if __name__ == "__main__":
    asyncio.run(test_websocket())