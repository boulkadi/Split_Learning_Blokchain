import torch
import torch.optim as optim
from ..models.client_model import ClientModel # Import relatif

class Client:
    def __init__(self, client_id, dataloader, model, address, private_key):
        self.client_id = client_id
        self.dataloader = dataloader
        self.model = model
        self.address = address
        self.private_key = private_key
        # Momentum ajouté pour matcher ton prototype
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        
        self.smashed_data = None

    def forward(self, data):
        self.model.train()
        self.smashed_data = self.model(data)
        return self.smashed_data

    def backward(self, gradient):
        self.optimizer.zero_grad()
        # On propage le gradient reçu du serveur à travers notre smashed_data local
        self.smashed_data.backward(gradient)
        self.optimizer.step()