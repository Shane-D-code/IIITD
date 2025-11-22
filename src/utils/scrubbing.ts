// PII scrubbing patterns
const EMAIL_REGEX = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
const PHONE_REGEX = /(\+?\d[\d\s\-\(\)]{8,15}\d)/g;
const CREDIT_CARD_REGEX = /\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}/g;
const NAME_REGEX = /\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b/g;

export interface ScrubResult {
  scrubbed: string;
  piiFound: string[];
}

export const scrubPII = (text: string): ScrubResult => {
  const piiFound: string[] = [];
  let scrubbed = text;

  // Log original for demo
  console.log('BEFORE scrubbing:', text.substring(0, 200) + '...');

  // Scrub emails
  const emails = text.match(EMAIL_REGEX);
  if (emails) {
    piiFound.push(...emails);
    scrubbed = scrubbed.replace(EMAIL_REGEX, '[EMAIL_REDACTED]');
  }

  // Scrub phone numbers
  const phones = text.match(PHONE_REGEX);
  if (phones) {
    piiFound.push(...phones);
    scrubbed = scrubbed.replace(PHONE_REGEX, '[PHONE_REDACTED]');
  }

  // Scrub credit cards
  const cards = text.match(CREDIT_CARD_REGEX);
  if (cards) {
    piiFound.push(...cards);
    scrubbed = scrubbed.replace(CREDIT_CARD_REGEX, '[CARD_REDACTED]');
  }

  // Scrub names
  const names = text.match(NAME_REGEX);
  if (names) {
    piiFound.push(...names);
    scrubbed = scrubbed.replace(NAME_REGEX, '[NAME_REDACTED]');
  }

  // Log scrubbed for demo
  console.log('AFTER scrubbing:', scrubbed.substring(0, 200) + '...');
  console.log('PII found and removed:', piiFound);

  return { scrubbed, piiFound };
};