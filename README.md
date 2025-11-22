# SilentScan Chrome Extension

Privacy-first phishing detection Chrome extension built with Vite + React + TypeScript.

## Key Features

- **Privacy-First**: All PII scrubbing happens locally, no raw data leaves device
- **Minimal Permissions**: Only storage and localhost access
- **Real-time Scanning**: Instant phishing risk detection
- **Hashed URLs**: All URLs are SHA-256 hashed before transmission
- **Demo-Ready**: Network tab shows only localhost requests with sanitized data

## Installation

1. Install dependencies:
```bash
npm install
```

2. Build the extension:
```bash
npm run build
```

3. Load in Chrome:
   - Open Chrome Extensions (chrome://extensions/)
   - Enable Developer mode
   - Click "Load unpacked"
   - Select the `dist` folder

## Development

```bash
npm run dev
```

## Privacy Architecture

1. **Content Script**: Extracts page data and immediately scrubs PII
2. **Local Hashing**: All URLs converted to SHA-256 hashes
3. **Sanitized Payloads**: Only cleaned data sent to localhost:8000
4. **No Cloud**: All communication stays on localhost for demo

## Demo Points

- Check Chrome DevTools Network tab during scan
- View console logs showing before/after PII scrubbing
- Inspect extension storage (only device token stored)
- All requests go to localhost:8000 with hashed data

## File Structure

```
src/
├── popup/           # React UI components
├── content/         # Content script for data extraction
├── background/      # Service worker
└── utils/          # Hashing and scrubbing utilities
```