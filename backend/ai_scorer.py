from transformers import pipeline
import torch

# Try phishing-specific models, fallback to toxicity detection
try:
    # Option 1: Phishing detection model
    classifier = pipeline(
        "text-classification",
        model="ealvaradob/bert-finetuned-phishing",
        device=0 if torch.cuda.is_available() else -1
    )
    MODEL_TYPE = "phishing"
except:
    try:
        # Option 2: Toxicity detection (good proxy for phishing)
        classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=0 if torch.cuda.is_available() else -1
        )
        MODEL_TYPE = "toxicity"
    except:
        # Option 3: Fallback to sentiment
        classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )
        MODEL_TYPE = "sentiment"

def ai_risk_score(text: str) -> dict:
    """Use AI model to score phishing risk"""
    try:
        result = classifier(text)
        label = result[0]['label']
        confidence = result[0]['score']
        
        if MODEL_TYPE == "phishing":
            # Direct phishing detection
            if label == "PHISHING" or label == "LABEL_1":
                risk_score = confidence
                reasoning = "AI detected phishing content"
            else:
                risk_score = 1 - confidence
                reasoning = "AI detected legitimate content"
                
        elif MODEL_TYPE == "toxicity":
            # Toxicity as phishing proxy
            if label == "TOXIC":
                risk_score = confidence * 0.9
                reasoning = "AI detected toxic/threatening language"
            else:
                risk_score = (1 - confidence) * 0.2
                reasoning = "AI detected non-toxic content"
                
        else:
            # Sentiment fallback
            if label == 'LABEL_0':  # Negative
                risk_score = confidence * 0.7
                reasoning = "AI detected negative tone"
            else:
                risk_score = confidence * 0.3
                reasoning = "AI detected neutral/positive tone"
        
        return {
            "ai_score": min(risk_score, 1.0),
            "ai_confidence": confidence,
            "ai_reasoning": f"{reasoning} ({MODEL_TYPE} model)"
        }
    except:
        return {"ai_score": 0.0, "ai_confidence": 0.0, "ai_reasoning": "AI model unavailable"}