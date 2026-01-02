import torch
import hashlib

class SplitModel(torch.nn.Module):
    """Classe de base pour ajouter des fonctionnalités de hachage aux modèles"""
    
    def get_model_hash(self):
        """Génère un hash court de l'état actuel du modèle pour la blockchain"""
        state_dict_str = str(self.state_dict()).encode()
        return hashlib.sha256(state_dict_str).hexdigest()[:16]