import torch
from web3 import Web3
from src.blockchain.blockchain_code import deploy_registry, BlockchainManager
from src.blockchain.models import ClientModel, ServerModel
from src.blockchain.data import MNISTLoader, get_dataloader
from src.blockchain.core import Client, Server, Coordinator
from src.blockchain.utils import Logger

def main():
    # 1. Connexion à Ganache
    GANACHE_URL = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
    if not w3.is_connected():
        Logger.error("Ganache n'est pas lancé sur http://127.0.0.1:7545")
        return

    # Récupérer les comptes Ganache (les 3 premiers pour les clients, le 4ème pour le deployer)
    accounts = w3.eth.accounts
    private_keys = [
        "0xfd372d3e2bdb4497923defa85f34835f0aabcc400d25350c1e804ad756815ac9",
        "0x81382c8d9526e6a5bab02cb2b4ec1359ba08af34f7819496d8085180618bd79a", 
        "0x3294d9e12bb070069ccaaef44567b074d0fa483b48f5733428cec6bc1afd834c", 
        "0xf58cad0c02d7ad3bbc00cd3e56a9cace9c38a1c208091d488d36f35ededa47e8"
    ]
    
    # 2. Déploiement du Smart Contract
    Logger.info("Déploiement du Smart Contract...")
    # On utilise le premier compte pour déployer
    contract_address, abi = deploy_registry(private_keys[0], accounts[0])
    Logger.success(f"Contrat déployé à l'adresse : {contract_address}")

    # 3. Initialisation du Blockchain Manager
    bm = BlockchainManager(GANACHE_URL)
    bm.load_contract(contract_address, abi)

    # 4. Préparation des données
    loader = MNISTLoader()
    train_set, _ = loader.get_full_datasets()
    subsets = loader.split_data(train_set, num_clients=3)

    # 5. Création des entités (Clients & Serveur)
    server_model = ServerModel()
    server = Server(server_model)

    clients = []
    for i in range(3):
        idx = i + 1
        client_dataloader = get_dataloader(subsets[i], batch_size=32)
        c = Client(
            client_id=i, 
            dataloader=client_dataloader, 
            model=ClientModel(), 
            address=accounts[idx], 
            private_key=private_keys[idx]
        )
        clients.append(c)

    # 6. Lancement de l'entraînement
    coordinator = Coordinator(clients, server, bm)
    
    num_rounds = 5
    for r in range(1, num_rounds + 1):
        coordinator.run_round(r)

    Logger.success("Entraînement et enregistrement Blockchain terminés !")

if __name__ == "__main__":
    main()