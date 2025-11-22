import torch

print("=== GPU Check ===")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA device count: {torch.cuda.device_count()}")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")
else:
    print("No GPU available - using CPU")

# Test model loading with GPU
try:
    from transformers import pipeline
    classifier = pipeline(
        "text-classification",
        model="ealvaradob/bert-finetuned-phishing",
        device=0 if torch.cuda.is_available() else -1
    )
    print(f"Model loaded on: {'GPU' if torch.cuda.is_available() else 'CPU'}")
except Exception as e:
    print(f"Model loading failed: {e}")
    print("Falling back to toxicity model...")
    try:
        classifier = pipeline(
            "text-classification", 
            model="unitary/toxic-bert",
            device=0 if torch.cuda.is_available() else -1
        )
        print("Toxicity model loaded successfully")
    except Exception as e2:
        print(f"Toxicity model also failed: {e2}")