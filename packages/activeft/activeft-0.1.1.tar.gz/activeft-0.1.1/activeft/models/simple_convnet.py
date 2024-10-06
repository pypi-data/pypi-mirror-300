import torch
from torch import nn


class SimpleCNN(nn.Module):
    def __init__(self, input_channels, output_channels, k):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(32 * 28 * 28, k)
        self.fc2 = nn.Linear(k, output_channels, bias=False)

    @property
    def final_layer(self):
        return self.fc2

    def logits(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x

    def forward(self, x):
        x = self.logits(x)
        x = self.fc2(x)
        x = torch.nn.functional.softmax(x, dim=1)
        return x

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        outputs = self(x)
        _, predicted = torch.max(outputs.data, dim=1)
        return predicted
