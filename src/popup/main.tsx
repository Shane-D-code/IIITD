import React from 'react';
import { createRoot } from 'react-dom/client';

interface LinkRisk {
  url_hash: string;
  anchor_text: string;
  domain: string;
  risk_level: 'clean' | 'suspicious' | 'high_risk';
  reasons: string[];
}

interface ScanResult {
  status: string;
  links_analyzed: number;
  risks_found: LinkRisk[];
}

const Popup: React.FC = () => {
  const [isRegistered, setIsRegistered] = React.useState(false);
  const [isScanning, setIsScanning] = React.useState(false);
  const [scanResult, setScanResult] = React.useState<ScanResult | null>(null);
  const [selectedRisk, setSelectedRisk] = React.useState<LinkRisk | null>(null);
  const [deviceToken, setDeviceToken] = React.useState<string>('');

  React.useEffect(() => {
    checkRegistration();
  }, []);

  const checkRegistration = async () => {
    const storage = await chrome.storage.local.get(['device_token']);
    if (storage.device_token) {
      setIsRegistered(true);
      setDeviceToken(storage.device_token);
    }
  };

  const registerDevice = async () => {
    try {
      const mockToken = 'demo_' + Date.now();
      await chrome.storage.local.set({ device_token: mockToken });
      setDeviceToken(mockToken);
      setIsRegistered(true);
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  const scanPage = async () => {
    setIsScanning(true);
    setScanResult(null);

    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (!tab.id) return;

      const scanData = await chrome.tabs.sendMessage(tab.id, { action: 'scan-page' });

      // Mock response for demo
      const result: ScanResult = {
        status: 'completed',
        links_analyzed: scanData.links.length,
        risks_found: scanData.links.slice(0, 3).map((link: any, index: number) => ({
          url_hash: link.url_hash,
          anchor_text: link.anchor_text,
          domain: link.domain,
          risk_level: index === 0 ? 'high_risk' : index === 1 ? 'suspicious' : 'clean',
          reasons: index === 0 ? ['Domain created recently', 'Suspicious keywords'] : 
                   index === 1 ? ['Unusual domain pattern'] : ['No issues detected']
        }))
      };

      setScanResult(result);
    } catch (error) {
      console.error('Scan failed:', error);
      setScanResult({
        status: 'completed',
        links_analyzed: 0,
        risks_found: []
      });
    } finally {
      setIsScanning(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high_risk': return '#ef4444';
      case 'suspicious': return '#f59e0b';
      case 'clean': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getRiskLabel = (level: string) => {
    switch (level) {
      case 'high_risk': return 'High Risk';
      case 'suspicious': return 'Suspicious';
      case 'clean': return 'Clean';
      default: return 'Unknown';
    }
  };

  return (
    <>
      <div style={{ marginBottom: '25px' }}>
        <h1 style={{ margin: '0 0 8px 0', fontSize: '28px', color: '#4c1d95', fontWeight: '700' }}>
          🛡️ SilentScan
        </h1>
        <p style={{ margin: 0, fontSize: '14px', color: '#6b7280', fontWeight: '500' }}>
          Privacy-first phishing detection
        </p>
      </div>

      {!isRegistered && (
        <div style={{ marginBottom: '25px' }}>
          <p style={{ fontSize: '16px', color: '#4b5563', marginBottom: '20px', fontWeight: '500' }}>
            Register your device to start scanning
          </p>
          <button
            onClick={registerDevice}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              fontSize: '16px',
              fontWeight: '600'
            }}
          >
            🔐 Register Device
          </button>
        </div>
      )}

      {isRegistered && (
        <>
          <div style={{ marginBottom: '25px' }}>
            <button
              onClick={scanPage}
              disabled={isScanning}
              style={{
                background: isScanning ? 'linear-gradient(135deg, #9ca3af 0%, #6b7280 100%)' : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                color: 'white',
                fontSize: '18px',
                fontWeight: '700',
                padding: '15px 30px'
              }}
            >
              {isScanning ? '🔍 Scanning...' : '🔍 Scan Page'}
            </button>
          </div>

          {scanResult && (
            <div className="results-container">
              <div style={{ 
                background: 'rgba(255,255,255,0.9)', 
                padding: '20px', 
                borderRadius: '15px',
                marginBottom: '20px',
                boxShadow: '0 4px 15px rgba(0,0,0,0.05)'
              }}>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '16px' }}>
                  Scan Results
                </h3>
                <p style={{ margin: '0', fontSize: '14px', color: '#6b7280' }}>
                  Analyzed {scanResult.links_analyzed} links • 
                  Found {scanResult.risks_found.length} potential risks
                </p>
              </div>

              <div className="scrollable">
                {scanResult.risks_found.map((risk, index) => (
                  <div
                    key={index}
                    className="risk-item"
                    onClick={() => setSelectedRisk(risk)}
                    style={{
                      border: `2px solid ${getRiskColor(risk.risk_level)}`,
                      borderRadius: '15px',
                      padding: '15px',
                      marginBottom: '12px',
                      cursor: 'pointer',
                      background: 'rgba(255,255,255,0.9)',
                      boxShadow: '0 2px 10px rgba(0,0,0,0.05)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '12px', fontWeight: '600' }}>
                        {risk.domain}
                      </span>
                      <span style={{
                        background: getRiskColor(risk.risk_level),
                        color: 'white',
                        padding: '2px 8px',
                        borderRadius: '12px',
                        fontSize: '10px'
                      }}>
                        {getRiskLabel(risk.risk_level)}
                      </span>
                    </div>
                    <p style={{ 
                      margin: '5px 0 0 0', 
                      fontSize: '11px', 
                      color: '#6b7280',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}>
                      {risk.anchor_text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="device-info">
            Device: {deviceToken.substring(0, 12)}...
          </div>
        </>
      )}

      {selectedRisk && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3 style={{ margin: '0 0 15px 0', fontSize: '16px' }}>
              Risk Details
            </h3>
            <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
              <strong>Domain:</strong> {selectedRisk.domain}
            </p>
            <p style={{ margin: '0 0 10px 0', fontSize: '14px' }}>
              <strong>Risk Level:</strong> {getRiskLabel(selectedRisk.risk_level)}
            </p>
            <p style={{ margin: '0 0 15px 0', fontSize: '14px' }}>
              <strong>Reasons:</strong>
            </p>
            <ul style={{ margin: '0 0 20px 0', paddingLeft: '20px' }}>
              {selectedRisk.reasons.map((reason, index) => (
                <li key={index} style={{ fontSize: '12px', marginBottom: '5px' }}>
                  {reason}
                </li>
              ))}
            </ul>
            <button
              onClick={() => setSelectedRisk(null)}
              style={{
                background: '#6b7280',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px'
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Popup />);
}