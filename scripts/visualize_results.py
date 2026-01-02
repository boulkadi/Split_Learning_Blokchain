import matplotlib.pyplot as plt
import os
from datetime import datetime
from src.blockchain.blockchain_code.deployer import load_contract_info
from src.blockchain.blockchain_code.blockchain_manager import BlockchainManager
from src.blockchain.utils.logger import Logger
from src.blockchain.blockchain_code import config

def visualize_blockchain_data():
    # 1. Chargement des informations du contrat
    address, abi = load_contract_info()
    if not address:
        Logger.error("Fichier contract_info.json introuvable. Lancez d'abord train.py")
        return

    # 2. Connexion à Ganache et initialisation du contrat
    bm = BlockchainManager("http://127.0.0.1:7545") 
    bm.load_contract(address, abi)
    
    Logger.info(f"Lecture du registre à l'adresse : {address}")

    # 3. Extraction des adresses clients
    clients = bm.contract.functions.getAllClients().call()
    
    if not clients:
        Logger.error("Aucune donnée disponible sur la blockchain.")
        return

    # Création de la figure
    plt.figure(figsize=(14, 6))
    
    for client_addr in clients:
        # Extraction de l'historique via le contrat
        count = bm.contract.functions.getHistoryCount(client_addr).call()
        rounds, accs, losses = [], [], []

        for i in range(count):
            # record = [round, hash, accuracy, loss, timestamp]
            record = bm.contract.functions.history(client_addr, i).call()
            rounds.append(record[0])
            accs.append(record[2] / config.ACCURACY_PRECISION)
            losses.append(record[3] / config.LOSS_PRECISION)

        # Graphique 1 : Accuracy
        plt.subplot(1, 2, 1)
        plt.plot(rounds, accs, marker='o', label=f"Client...{client_addr[-6:]}")
        
        # Graphique 2 : Loss
        plt.subplot(1, 2, 2)
        plt.plot(rounds, losses, marker='x', linestyle='--', label=f"Client...{client_addr[-6:]}")

    # --- Mise en forme du graphique ---
    
    # Subplot Accuracy
    plt.subplot(1, 2, 1)
    plt.title("Évolution de la Précision (Blockchain)")
    plt.xlabel("Round")
    plt.ylabel("Accuracy (%)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Subplot Loss
    plt.subplot(1, 2, 2)
    plt.title("Évolution de la Perte (Blockchain)")
    plt.xlabel("Round")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    # --- Sauvegarde du graphique ---

    # Définition du chemin de sauvegarde (racine_projet/data/images)
    # On remonte de scripts/ vers la racine
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(base_dir, 'data', 'images')
    
    # Création du dossier s'il n'existe pas
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        Logger.info(f" Création du répertoire de sauvegarde : {save_dir}")

    # Génération d'un nom unique avec la date et l'heure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"split_learning_results_{timestamp}.png"
    save_path = os.path.join(save_dir, filename)

    # Sauvegarde impérative AVANT plt.show()
    plt.savefig(save_path, dpi=300)
    Logger.success(f" Graphe sauvegardé avec succès : {save_path}")

    # Affichage à l'écran
    plt.show()

if __name__ == "__main__":
    visualize_blockchain_data()