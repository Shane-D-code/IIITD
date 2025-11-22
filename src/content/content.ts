// Inline utilities to avoid import issues
const sha256 = async (text: string): Promise<string> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
};

const scrubPII = (text: string) => {
  const EMAIL_REGEX = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
  const PHONE_REGEX = /(\+?\d[\d\s\-\(\)]{8,15}\d)/g;
  const CREDIT_CARD_REGEX = /\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}/g;
  const NAME_REGEX = /\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b/g;
  
  console.log('BEFORE scrubbing:', text.substring(0, 200) + '...');
  
  let scrubbed = text
    .replace(EMAIL_REGEX, '[EMAIL_REDACTED]')
    .replace(PHONE_REGEX, '[PHONE_REDACTED]')
    .replace(CREDIT_CARD_REGEX, '[CARD_REDACTED]')
    .replace(NAME_REGEX, '[NAME_REDACTED]');
  
  console.log('AFTER scrubbing:', scrubbed.substring(0, 200) + '...');
  
  return { scrubbed, piiFound: [] };
};

interface LinkData {
  url_hash: string;
  anchor_text: string;
  domain: string;
}

interface ScanPayload {
  device_token: string;
  page_title: string;
  page_url_hash: string;
  page_text_sample: string;
  links: LinkData[];
  timestamp: number;
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.action === 'scan-page') {
    scanCurrentPage().then(sendResponse);
    return true; // Keep message channel open for async response
  }
});

async function scanCurrentPage(): Promise<ScanPayload> {
  console.log('🔍 Starting page scan...');

  // Extract page data
  const pageTitle = document.title;
  const pageUrl = window.location.href;
  const pageText = document.body.innerText;

  // Scrub PII from page text
  const { scrubbed: scrubbedText } = scrubPII(pageText);
  const textSample = scrubbedText.substring(0, 500); // First 500 chars

  // Extract and process links
  const linkElements = document.querySelectorAll('a[href]');
  const links: LinkData[] = [];

  for (const link of linkElements) {
    const href = (link as HTMLAnchorElement).href;
    const text = link.textContent?.trim() || '';
    
    if (href && href.startsWith('http')) {
      const { scrubbed: scrubbedAnchor } = scrubPII(text);
      
      links.push({
        url_hash: await sha256(href),
        anchor_text: scrubbedAnchor,
        domain: new URL(href).hostname
      });
    }
  }

  // Get device token from storage
  const storage = await chrome.storage.local.get(['device_token']);
  const deviceToken = storage.device_token || 'unregistered';

  const payload: ScanPayload = {
    device_token: deviceToken,
    page_title: pageTitle,
    page_url_hash: await sha256(pageUrl),
    page_text_sample: textSample,
    links: links.slice(0, 20), // Limit to first 20 links
    timestamp: Date.now()
  };

  console.log('📦 Scan payload prepared:', payload);
  return payload;
}