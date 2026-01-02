import torch.nn as nn
from .base_model import SplitModel

class ClientModel(SplitModel):
    def __init__(self):
        super(ClientModel, self).__init__()
        # Couches de convolution initiales (MNIST: 1 canal -> 32)
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        
    def forward(self, x):
        return self.features(x)  # Envoie les "Smashed Data" au serveur