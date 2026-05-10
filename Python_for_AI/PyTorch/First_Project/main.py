import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

torch.cuda.is_available()
torch.cuda.device_count()
torch.cuda.get_device_name(0)
torch.cuda.device(0)

arr = np.array([[1, 2, 3], [4, 5, 6]])

tensor = torch.Tensor([[1, 2, 3], [4, 5, 6]])
torch.ones((2, 3))
torch.rand((2, 4))
arr.shape
tensor = tensor.to("cpu")

tensor.sum()
tensor.numpy()
device = "cuda" if torch.cuda.is_available() else "cpu"
a = torch.tensor([2.0, 3.0], requires_grad=True)
b = torch.tensor([6.0, 4.0], requires_grad=True)
f = 3 * a**3 - b**2
f.backward(gradient=torch.tensor([1, 1]))
print(a.grad)
print(b.grad)


# ----------------------------------------------------------------------


X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_train_scaled_tensor = torch.from_numpy(X_train_scaled).float()
X_test_scaled_tensor = torch.from_numpy(X_test_scaled).float()
y_train_tensor = torch.from_numpy(y_train).float().unsqueeze(1)
y_test_tensor = torch.from_numpy(y_test).float().unsqueeze(1)

train_dataset = TensorDataset(X_train_scaled_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


class BCnet(nn.Module):
    def __init__(self):
        super(BCnet, self).__init__()
        self.fc1 = nn.Linear(30, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.sigmoid(self.fc3(x))
        return x


model = BCnet()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
epochs = 100
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for x_batch, y_batch in train_loader:
        optimizer.zero_grad()

        preds = model(x_batch)
        loss = criterion(preds, y_batch)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"Epoch {epoch + 1}: Loss was {running_loss / len(train_loader)}")
with torch.no_grad():
    model.eval()
    preds = model(X_test_scaled_tensor)
    loss = criterion(preds, y_test_tensor).item()
    accuracy = ((preds >= 0.5) == y_test_tensor).float().mean().item()
    accuracy
