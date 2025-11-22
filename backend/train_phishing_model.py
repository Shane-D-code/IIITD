from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset
import pandas as pd

# Sample phishing training data (you'd need a real dataset)
PHISHING_DATA = [
    {"text": "URGENT! Your account will be suspended! Click here now!", "label": 1},
    {"text": "Congratulations! You've won $10000! Claim now!", "label": 1},
    {"text": "Your payment is due. Please update your information.", "label": 1},
    {"text": "Hello, how are you doing today?", "label": 0},
    {"text": "Meeting scheduled for tomorrow at 3 PM.", "label": 0},
    {"text": "Thank you for your purchase. Receipt attached.", "label": 0},
]

class PhishingDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

def train_phishing_model():
    """Train a custom phishing detection model"""
    # Load base model
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Prepare data
    texts = [item["text"] for item in PHISHING_DATA]
    labels = [item["label"] for item in PHISHING_DATA]
    
    dataset = PhishingDataset(texts, labels, tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir='./phishing_model',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        save_steps=10_000,
        save_total_limit=2,
    )
    
    # Train
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
    )
    
    trainer.train()
    trainer.save_model()
    print("✓ Custom phishing model trained and saved!")

if __name__ == "__main__":
    # Note: This is just a demo - you'd need a real phishing dataset
    print("Demo training script - needs real phishing dataset")
    # train_phishing_model()