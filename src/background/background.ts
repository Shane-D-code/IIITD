// Background service worker for SilentScan
console.log('🚀 SilentScan background service worker loaded');

// Handle extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('📦 SilentScan installed');
    // Set default storage values
    chrome.storage.local.set({
      scan_count: 0,
      last_scan: null
    });
  }
});

// Handle messages between popup and content script
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  console.log('📨 Background received message:', message);
  
  if (message.action === 'get-tab-info') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        sendResponse({
          url: tabs[0].url,
          title: tabs[0].title,
          id: tabs[0].id
        });
      }
    });
    return true;
  }
});