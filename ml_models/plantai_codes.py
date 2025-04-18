import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import os

DATASET_PATH = 'C:/DTI_NAVYA/Niramay/media/Segmented Medicinal Leaf Images'
MODEL_PATH = 'C:/DTI_NAVYA/Niramay/ml_models/plant_model.pth'
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder(DATASET_PATH, transform=transform)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_set, test_set = torch.utils.data.random_split(dataset, [train_size, test_size])
train_loader = torch.utils.data.DataLoader(train_set, batch_size=32, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=32)

# Load Pretrained Model
model = models.mobilenet_v2(pretrained=True)
model.classifier[1] = nn.Linear(model.last_channel, len(dataset.classes))

# Freeze base layers
for param in model.features.parameters():
    param.requires_grad = False

# Training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {running_loss:.4f}")

torch.save(model.state_dict(), MODEL_PATH)
print(f"✅ PyTorch model saved to: {MODEL_PATH}")
