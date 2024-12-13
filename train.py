import numpy as np
import random
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.model_selection import train_test_split

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet, count_parameters

# Configuration
class Config:
    RANDOM_SEED = 42
    NUM_EPOCHS = 2000
    BATCH_SIZE = 64
    LEARNING_RATE = 0.001
    HIDDEN_SIZE = 128
    DROPOUT_RATE = 0.3
    EARLY_STOPPING_PATIENCE = 100

# Set random seeds for reproducibility
random.seed(Config.RANDOM_SEED)
np.random.seed(Config.RANDOM_SEED)
torch.manual_seed(Config.RANDOM_SEED)

# Load intents data
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Prepare data with improved preprocessing
def prepare_training_data(intents):
    all_words, tags, patterns = [], [], []
    ignore_words = ['?', '.', '!', ',']

    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            words = tokenize(pattern)
            all_words.extend(words)
            patterns.append((words, tag))

    # Improved stemming and filtering
    all_words = [stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    # Bag of words and labels
    X, y = [], []
    for (pattern_sentence, tag) in patterns:
        X.append(bag_of_words(pattern_sentence, all_words))
        y.append(tags.index(tag))

    X, y = np.array(X), np.array(y)
    
    return X, y, all_words, tags

# Prepare data
X, y, all_words, tags = prepare_training_data(intents)

# Split data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=Config.RANDOM_SEED)

# Dataset definition
class ChatDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.LongTensor(y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

    def __len__(self):
        return len(self.X)

# Data loaders
train_dataset = ChatDataset(X_train, y_train)
val_dataset = ChatDataset(X_val, y_val)

train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model, loss, optimizer, scheduler
model = NeuralNet(
    input_size=len(all_words), 
    hidden_size=Config.HIDDEN_SIZE, 
    num_classes=len(tags),
    dropout_rate=Config.DROPOUT_RATE
).to(device)

print(f"Total trainable parameters: {count_parameters(model)}")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=1e-5)
scheduler = ReduceLROnPlateau(optimizer, 'min', patience=10, factor=0.5, verbose=False)

# Training loop with validation and early stopping
best_val_loss = float('inf')
early_stopping_counter = 0

print(f"Starting training on {device}")
for epoch in range(Config.NUM_EPOCHS):
    model.train()
    total_train_loss = 0
    
    for words, labels in train_loader:
        words, labels = words.to(device), labels.to(device)
        
        # Forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)
        
        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_train_loss += loss.item()
    
    # Validation
    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for words, labels in val_loader:
            words, labels = words.to(device), labels.to(device)
            outputs = model(words)
            val_loss = criterion(outputs, labels)
            total_val_loss += val_loss.item()
    
    avg_train_loss = total_train_loss / len(train_loader)
    avg_val_loss = total_val_loss / len(val_loader)
    
    scheduler.step(avg_val_loss)
    
    # Early stopping
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        early_stopping_counter = 0
        
        # Prepare model data BEFORE saving
        model_data = {
            "model_state": model.state_dict(),
            "input_size": len(all_words),
            "hidden_size": Config.HIDDEN_SIZE,
            "output_size": len(tags),
            "all_words": all_words,
            "tags": tags,
        }
        
        # Save best model
        torch.save(model_data, "best_model.pth")
    else:
        early_stopping_counter += 1
    
    # Print progress
    if (epoch + 1) % 50 == 0:
        print(f"Epoch [{epoch+1}/{Config.NUM_EPOCHS}], "
              f"Train Loss: {avg_train_loss:.4f}, "
              f"Val Loss: {avg_val_loss:.4f}")
    
    # Early stopping condition
    if early_stopping_counter >= Config.EARLY_STOPPING_PATIENCE:
        print("Early stopping triggered")
        break

# Final model save
model_data = {
    "model_state": model.state_dict(),
    "input_size": len(all_words),
    "hidden_size": Config.HIDDEN_SIZE,
    "output_size": len(tags),
    "all_words": all_words,
    "tags": tags,
}

torch.save(model_data, "data.pth")
print("Training complete. Model saved to 'data.pth'")