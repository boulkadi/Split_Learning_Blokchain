import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import os

class MNISTLoader:
    def __init__(self, data_path=None):
        if data_path is None:
            # On remonte de deux niveaux depuis src/blockchain/data/ pour arriver à la racine
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            self.data_path = os.path.join(base_dir, 'data', 'datasets')
        else:
            self.data_path = data_path
        # Transformation standard pour MNIST
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

    def get_full_datasets(self):
        """Télécharge et retourne les datasets complets"""
        mnist_folder = os.path.join(self.data_path, 'MNIST')
        exists = os.path.exists(mnist_folder)
        if exists:
            print(f" Données MNIST trouvées dans {self.data_path}, chargement local...")
        else:
            print(f" Données non trouvées. Téléchargement de MNIST dans {self.data_path}...")
        train_set = datasets.MNIST(self.data_path, train=True, download=True, transform=self.transform)
        test_set = datasets.MNIST(self.data_path, train=False, download=True, transform=self.transform)
        return train_set, test_set

    def split_data(self, dataset, num_clients):
        """Divise le dataset en parts égales pour chaque client"""
        total_samples = len(dataset)
        samples_per_client = total_samples // num_clients
        client_subsets = []

        for i in range(num_clients):
            start = i * samples_per_client
            end = start + samples_per_client
            indices = list(range(start, end))
            client_subsets.append(Subset(dataset, indices))
        
        return client_subsets