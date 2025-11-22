# IIITD - SilentScan Phishing Detection System

Privacy-first phishing detection system with Chrome extension and AI-powered backend.

## Components

### Backend (FastAPI)
- **AI Phishing Detection**: BERT model fine-tuned for phishing
- **Fuzzy Logic**: Advanced risk scoring
- **WebSocket**: Real-time notifications
- **Privacy-First**: Only hashed data stored
- **GPU Accelerated**: RTX 4060 support

### Chrome Extension
- **Privacy-First**: All PII scrubbing happens locally
- **Real-time Scanning**: Instant phishing risk detection
- **Hashed URLs**: SHA-256 hashed before transmission
- **Demo-Ready**: Network tab shows sanitized data

## Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

### Chrome Extension
```bash
npm install
npm run build
# Load dist/ folder in Chrome Extensions
```

## Architecture

1. **Content Script**: Extracts and scrubs PII locally
2. **Backend API**: AI + Fuzzy Logic risk scoring
3. **WebSocket**: Real-time dashboard notifications
4. **Database**: Only hashed URLs and numeric scores
