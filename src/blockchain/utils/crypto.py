import hashlib
import json

def generate_hash(data_string):
    """Génère un SHA-256 court pour n'importe quelle chaîne"""
    return hashlib.sha256(data_string.encode()).hexdigest()[:16]

def hash_model_weights(model_state_dict):
    """Crée une empreinte numérique des poids du modèle"""
    weights_str = str(model_state_dict)
    return generate_hash(weights_str)