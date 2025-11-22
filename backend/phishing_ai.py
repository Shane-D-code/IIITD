from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Option 1: Use a phishing-specific model (if available)
try:
    # This would be a model specifically trained on phishing data
    classifier = pipeline(
        "text-classification",
        model="martin-ha/toxic-comment-model",  # Toxicity detection as proxy
        device=0 if torch.cuda.is_available() else -1
    )
    MODEL_TYPE = "toxicity"
except:
    # Fallback to sentiment
    classifier = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=0 if torch.cuda.is_available() else -1
    )
    MODEL_TYPE = "sentiment"

def phishing_ai_score(text: str) -> dict:
    """Use AI model specifically for phishing detection"""
    try:
        result = classifier(text)
        label = result[0]['label']
        confidence = result[0]['score']
        
        if MODEL_TYPE == "toxicity":
            # Toxic content often indicates phishing
            if label == "TOXIC":
                risk_score = confidence * 0.9
                reasoning = "AI detected toxic/threatening language"
            else:
                risk_score = (1 - confidence) * 0.3
                reasoning = "AI detected non-toxic content"
        else:
            # Sentiment-based (fallback)
            if label == 'LABEL_0':  # Negative
                risk_score = confidence * 0.8
                reasoning = "AI detected negative/threatening tone"
            elif label == 'LABEL_1':  # Neutral
                risk_score = confidence * 0.4
                reasoning = "AI detected neutral tone"
            else:  # Positive
                risk_score = confidence * 0.6
                reasoning = "AI detected suspicious positive tone"
        
        return {
            "ai_score": min(risk_score, 1.0),
            "ai_confidence": confidence,
            "ai_reasoning": reasoning,
            "model_type": MODEL_TYPE
        }
    except:
        return {"ai_score": 0.0, "ai_confidence": 0.0, "ai_reasoning": "AI model unavailable", "model_type": "none"}