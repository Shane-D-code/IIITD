# SilentScan Demo Instructions

## Installation Steps

1. **Build the Extension** (Already Done)
   ```bash
   cd silentscan-extension
   npm install
   npm run build
   ```

2. **Load in Chrome**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select the `dist` folder from this project

3. **Pin the Extension**
   - Click the puzzle piece icon in Chrome toolbar
   - Pin SilentScan for easy access

## Demo Script

### 1. Show Privacy Architecture
- Open Chrome DevTools (F12) → Network tab
- Navigate to any website (e.g., amazon.com, github.com)
- Click the SilentScan extension icon

### 2. Device Registration Demo
- Click "Register Device" 
- Show that only a device token is stored (no personal data)
- Check Chrome DevTools → Application → Storage → Extension storage

### 3. Page Scanning Demo
- Click "🔍 Scan Page"
- **Point out in Network tab**: Only localhost:8000 requests (no cloud!)
- **Show Console logs**: BEFORE/AFTER PII scrubbing
- **Highlight**: URLs are hashed, no raw data transmitted

### 4. Risk Detection Demo
- Scan results show color-coded risk levels:
  - 🔴 High Risk: Suspicious domains, recent registration
  - 🟡 Suspicious: Unusual patterns
  - 🟢 Clean: No issues detected
- Click on risk badges to see detailed explanations

### 5. Privacy Proof Points
- **Network Tab**: Only localhost requests with hashed payloads
- **Console Logs**: PII scrubbing in action
- **Extension Storage**: Only device token, no sensitive data
- **Minimal Permissions**: Only storage + localhost access

## Key Demo Messages

1. **"No Raw Data Leaves Your Device"** - All URLs are SHA-256 hashed
2. **"PII Scrubbed Locally"** - Emails, phones, names removed before processing
3. **"Minimal Permissions"** - No webRequest, no broad host permissions
4. **"Localhost Only"** - All communication stays local for demo
5. **"Startup Ready"** - Device registration system for scaling

## Technical Highlights

- **Vite + React + TypeScript**: Modern development stack
- **Manifest V3**: Latest Chrome extension standard
- **Web Crypto API**: Native browser hashing (no external libs)
- **Real-time UI**: Instant feedback and loading states
- **Error Handling**: Graceful fallbacks for demo scenarios

## Troubleshooting

If the extension doesn't load:
1. Check that all files are in `dist/` folder
2. Verify manifest.json is present
3. Reload the extension in chrome://extensions/
4. Check browser console for errors

## Startup Pitch Points

- **Privacy-First**: Zero trust architecture
- **Scalable**: Device registration system ready
- **Demo-Proof**: Visible privacy in DevTools
- **Production-Ready**: Error handling, loading states
- **Modern Stack**: Hackathon-friendly tech choices