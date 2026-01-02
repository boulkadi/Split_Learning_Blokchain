# Paramètres de connexion Ganache
GANACHE_URL = "http://127.0.0.1:7545"

# Ces valeurs seront mises à jour après le premier déploiement
CONTRACT_ADDRESS = None 
ABI = None 

# Paramètres de conversion (pour gérer les floats en uint256)
ACCURACY_PRECISION = 100    # 95.55% -> 9555
LOSS_PRECISION = 10000      # 0.1234 -> 1234