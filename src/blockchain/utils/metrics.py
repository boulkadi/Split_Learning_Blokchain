import torch

def calculate_accuracy(outputs, labels):
    """Calcule le pourcentage de bonnes prédictions"""
    _, predicted = torch.max(outputs.data, 1)
    total = labels.size(0)
    correct = (predicted == labels).sum().item()
    return 100 * correct / total

def format_blockchain_data(value, precision=100):
    """Prépare un float pour le stockage uint256 sur Solidity"""
    return int(value * precision)