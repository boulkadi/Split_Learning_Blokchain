import os

# Fournit le chemin absolu vers le fichier .sol pour le compilateur
CONTRACTS_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_SOL_PATH = os.path.join(CONTRACTS_DIR, "TrainingRegistry.sol")