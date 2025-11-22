import numpy as np

def fuzzy_membership(value, low, medium, high):
    """Calculate fuzzy membership for low/medium/high categories"""
    if value <= low:
        return {"low": 1.0, "medium": 0.0, "high": 0.0}
    elif value <= medium:
        # Transition from low to medium
        medium_membership = (value - low) / (medium - low)
        low_membership = 1.0 - medium_membership
        return {"low": low_membership, "medium": medium_membership, "high": 0.0}
    elif value <= high:
        # Transition from medium to high
        high_membership = (value - medium) / (high - medium)
        medium_membership = 1.0 - high_membership
        return {"low": 0.0, "medium": medium_membership, "high": high_membership}
    else:
        return {"low": 0.0, "medium": 0.0, "high": 1.0}

def fuzzy_risk_score(url_risk, text_risk, ai_risk):
    """Apply fuzzy logic to combine different risk factors"""
    
    # Define fuzzy sets for each risk type
    url_fuzzy = fuzzy_membership(url_risk, 0.3, 0.6, 0.9)
    text_fuzzy = fuzzy_membership(text_risk, 0.2, 0.5, 0.8)
    ai_fuzzy = fuzzy_membership(ai_risk, 0.3, 0.6, 0.9)
    
    # Fuzzy rules (simplified)
    rules = [
        # If URL is high OR text is high OR AI is high → high risk
        min(max(url_fuzzy["high"], text_fuzzy["high"], ai_fuzzy["high"]), 1.0),
        
        # If URL is medium AND text is medium → medium-high risk
        min(url_fuzzy["medium"], text_fuzzy["medium"]) * 0.7,
        
        # If AI is high AND (URL medium OR text medium) → high risk
        min(ai_fuzzy["high"], max(url_fuzzy["medium"], text_fuzzy["medium"])) * 0.9
    ]
    
    # Defuzzification - take maximum activation
    final_risk = max(rules)
    
    # Generate fuzzy reasoning
    reasoning = []
    if url_fuzzy["high"] > 0.5:
        reasoning.append("Fuzzy logic: High URL risk detected")
    if text_fuzzy["high"] > 0.5:
        reasoning.append("Fuzzy logic: High text risk detected")
    if ai_fuzzy["high"] > 0.5:
        reasoning.append("Fuzzy logic: High AI risk detected")
    if final_risk > 0.7:
        reasoning.append("Fuzzy logic: Combined high risk assessment")
    
    return {
        "fuzzy_score": min(final_risk, 1.0),
        "fuzzy_reasoning": reasoning,
        "fuzzy_breakdown": {
            "url_membership": url_fuzzy,
            "text_membership": text_fuzzy,
            "ai_membership": ai_fuzzy
        }
    }