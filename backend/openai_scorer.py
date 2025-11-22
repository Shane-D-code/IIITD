import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_risk_score(text: str, urls: list) -> dict:
    """Use OpenAI to analyze phishing risk"""
    try:
        prompt = f"""
Analyze this content for phishing risk (0.0-1.0 score):
Text: {text}
URLs: {urls}

Return JSON: {{"score": 0.8, "reasoning": "explanation"}}
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return {
            "ai_score": result.get("score", 0.0),
            "ai_reasoning": result.get("reasoning", "AI analysis")
        }
    except:
        return {"ai_score": 0.0, "ai_reasoning": "AI unavailable"}