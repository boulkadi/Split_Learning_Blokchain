import torch

def get_dataloader(dataset, batch_size=32, shuffle=True):
    """Crée un DataLoader PyTorch à partir d'un subset"""
    return torch.utils.data.DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=shuffle
    )

def flatten_batch(data):
    """Exemple de fonction utilitaire pour redimensionner les images si besoin"""
    return data.view(data.size(0), -1)