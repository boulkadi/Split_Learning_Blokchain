import torch.nn as nn
from .base_model import SplitModel

class ServerModel(SplitModel):
    def __init__(self):
        super(ServerModel, self).__init__()
        # Reçoit 32 channels de 7x7 (après deux MaxPool sur 28x28)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 10)
        )
        
    def forward(self, x):
        return self.classifier(x)