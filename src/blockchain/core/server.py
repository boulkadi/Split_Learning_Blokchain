import torch
import torch.nn as nn
import torch.optim as optim

class Server:
    def __init__(self, model):
        self.model = model
        # On ajoute le momentum=0.9 comme dans ton prototype
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01, momentum=0.9)
        self.criterion = nn.CrossEntropyLoss()
        self.smashed_data = None

    def forward(self, smashed_data):
        self.model.train()
        # On détache et on active le calcul du gradient sur les données reçues
        self.smashed_data = smashed_data.detach().requires_grad_()
        output = self.model(self.smashed_data)
        return output

    def backward(self, labels):
        self.optimizer.zero_grad()
        # Recalcul de l'output pour s'assurer que le graphe est lié à self.smashed_data
        output = self.model(self.smashed_data)
        loss = self.criterion(output, labels)
        loss.backward()
        self.optimizer.step()

        # On récupère le gradient à renvoyer au client
        gradient = self.smashed_data.grad
        return gradient, loss.item()