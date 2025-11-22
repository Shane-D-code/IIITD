import re
import logging

logger = logging.getLogger(__name__)

# PII regex patterns
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PHONE_PATTERN = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
SSN_PATTERN = r'\b\d{3}-?\d{2}-?\d{4}\b'
CREDIT_CARD_PATTERN = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'

def scrub_pii(text: str) -> str:
    """
    Scrub PII from text and log scrubbing actions without content.
    """
    original_text = text
    scrubbed = False
    
    # Email addresses
    if re.search(EMAIL_PATTERN, text):
        text = re.sub(EMAIL_PATTERN, '[EMAIL]', text)
        scrubbed = True
    
    # Phone numbers
    if re.search(PHONE_PATTERN, text):
        text = re.sub(PHONE_PATTERN, '[PHONE]', text)
        scrubbed = True
    
    # SSN
    if re.search(SSN_PATTERN, text):
        text = re.sub(SSN_PATTERN, '[SSN]', text)
        scrubbed = True
    
    # Credit cards
    if re.search(CREDIT_CARD_PATTERN, text):
        text = re.sub(CREDIT_CARD_PATTERN, '[CREDIT_CARD]', text)
        scrubbed = True
    
    # Log scrubbing action without content
    if scrubbed:
        logger.info({"scrubbed": True})
    
    return text