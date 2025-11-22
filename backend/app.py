from fastapi import FastAPI, Depends, HTTPException, WebSocket, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import secrets
import hashlib
import hmac
import json
import asyncio
from datetime import datetime
from typing import Optional, List
import uvicorn

from models import get_db, Device, ScanResult
from pii_scrubber import scrub_pii

app = FastAPI()
security = HTTPBearer()

# Server secret for token hashing
SERVER_SECRET = secrets.token_bytes(32)

# WebSocket connections
connections = {}

def hash_token(token: str) -> str:
    return hmac.new(SERVER_SECRET, token.encode(), hashlib.sha256).hexdigest()

def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()

def calculate_risk_score(text: str, urls: List[str]) -> dict:
    score = 0.0
    reasons = []
    high_risk_links = 0
    
    # AI Analysis
    ai_score = 0.0
    try:
        from ai_scorer import ai_risk_score
        ai_result = ai_risk_score(text)
        ai_score = ai_result["ai_score"]
        score = max(score, ai_score)
        if ai_score > 0.3:
            reasons.append(ai_result["ai_reasoning"])
    except:
        pass  # Continue without AI if model fails
    
    # URL heuristics
    for url in urls:
        url_score = 0.0
        if not url.startswith('https://'):
            url_score += 0.3
            reasons.append("Non-HTTPS URL detected")
        
        # Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.bit']
        if any(tld in url for tld in suspicious_tlds):
            url_score += 0.4
            reasons.append("Suspicious domain extension")
        
        # Suspicious keywords in domain
        suspicious_keywords = ['secure', 'verify', 'update', 'confirm', 'urgent']
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            url_score += 0.3
            reasons.append("Suspicious domain keywords")
        
        if url_score > 0.5:
            high_risk_links += 1
        score = max(score, url_score)
    
    # Text heuristics
    urgency_phrases = ['urgent', 'immediate', 'expires today', 'act now', 'limited time']
    money_indicators = ['$', 'payment', 'refund', 'prize', 'winner', 'claim']
    
    text_lower = text.lower()
    for phrase in urgency_phrases:
        if phrase in text_lower:
            score += 0.2
            reasons.append("Urgency language detected")
            break
    
    for indicator in money_indicators:
        if indicator in text_lower:
            score += 0.3
            reasons.append("Financial request indicators")
            break
    
    # Separate risk components for fuzzy logic
    url_risk = 0.0
    text_risk = 0.0
    
    # Calculate URL risk component
    for url in urls:
        url_score = 0.0
        if not url.startswith('https://'):
            url_score += 0.3
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.bit']
        if any(tld in url for tld in suspicious_tlds):
            url_score += 0.4
        suspicious_keywords = ['secure', 'verify', 'update', 'confirm', 'urgent']
        if any(keyword in url.lower() for keyword in suspicious_keywords):
            url_score += 0.3
        url_risk = max(url_risk, url_score)
    
    # Calculate text risk component
    urgency_phrases = ['urgent', 'immediate', 'expires today', 'act now', 'limited time']
    money_indicators = ['$', 'payment', 'refund', 'prize', 'winner', 'claim']
    text_lower = text.lower()
    
    for phrase in urgency_phrases:
        if phrase in text_lower:
            text_risk += 0.2
            break
    for indicator in money_indicators:
        if indicator in text_lower:
            text_risk += 0.3
            break
    
    # Apply fuzzy logic
    try:
        from fuzzy_scorer import fuzzy_risk_score
        fuzzy_result = fuzzy_risk_score(url_risk, text_risk, ai_score)
        final_score = max(score, fuzzy_result["fuzzy_score"])
        reasons.extend(fuzzy_result["fuzzy_reasoning"])
    except:
        final_score = score
    
    return {
        "score": min(final_score, 1.0),
        "reasons": reasons,
        "high_risk_link_count": high_risk_links
    }

@app.post("/api/v1/devices/register")
async def register_device(db: Session = Depends(get_db)):
    device_token = secrets.token_urlsafe(48)
    hashed_token = hash_token(device_token)
    
    device = Device(token_hash=hashed_token)
    db.add(device)
    db.commit()
    
    return {"device_token": device_token}

@app.post("/api/v1/scan")
@app.post("/api/v1/analyze")  # Alias for tests
async def scan_content(
    payload: dict,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization")
    
    token = authorization.split(" ")[1]
    hashed_token = hash_token(token)
    
    device = db.query(Device).filter(Device.token_hash == hashed_token).first()
    if not device:
        raise HTTPException(401, "Invalid token")
    
    # Server-side scrub (defensive)
    sanitized_text = scrub_pii(payload.get("sanitized_text", ""))
    urls = payload.get("urls", [])
    
    # Calculate risk
    risk_data = calculate_risk_score(sanitized_text, urls)
    
    # Store scan result (hashed URLs only)
    scan_result = ScanResult(
        device_id=device.id,
        url_hashes=[hash_url(url) for url in urls],
        risk_score=risk_data["score"],
        high_risk_link_count=risk_data["high_risk_link_count"]
    )
    db.add(scan_result)
    db.commit()
    
    # Push WebSocket update
    if device.id in connections:
        summary = {
            "device_id": str(device.id),
            "timestamp": datetime.utcnow().isoformat(),
            "score": risk_data["score"],
            "high_risk_link_count": risk_data["high_risk_link_count"]
        }
        await connections[device.id].send_text(json.dumps(summary))
    
    return {
        "risk_score": risk_data["score"],
        "reasons": risk_data["reasons"],
        "high_risk_link_count": risk_data["high_risk_link_count"]
    }

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await websocket.accept()
    
    hashed_token = hash_token(token)
    db = next(get_db())
    device = db.query(Device).filter(Device.token_hash == hashed_token).first()
    
    if not device:
        await websocket.close(code=4001)
        return
    
    connections[device.id] = websocket
    
    try:
        while True:
            await websocket.receive_text()
    except:
        pass
    finally:
        connections.pop(device.id, None)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)