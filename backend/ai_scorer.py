from transformers import pipeline
import torch

# Force GPU usage if available
device = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'GPU' if device == 0 else 'CPU'}")

# Try phishing-specific models, fallback to toxicity detection
try:
    # Option 1: Phishing detection model
    classifier = pipeline(
        "text-classification",
        model="ealvaradob/bert-finetuned-phishing",
        device=device
    )
    MODEL_TYPE = "phishing"
    print(f"Loaded phishing model on {'GPU' if device == 0 else 'CPU'}")
except:
    try:
        # Option 2: Toxicity detection (good proxy for phishing)
        classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=device
        )
        MODEL_TYPE = "toxicity"
        print(f"Loaded toxicity model on {'GPU' if device == 0 else 'CPU'}")
    except:
        # Option 3: Fallback to sentiment
        classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=device
        )
        MODEL_TYPE = "sentiment"
        print(f"Loaded sentiment model on {'GPU' if device == 0 else 'CPU'}")

def ai_risk_score(text: str) -> dict:
    """Use AI model to score phishing risk"""
    try:
        print(f"GPU available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"Model device: {classifier.device}")
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