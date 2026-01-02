from web3 import Web3
from . import config

class BlockchainManager:
    def __init__(self, rpc_url=config.GANACHE_URL):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            print(" Erreur: Impossible de se connecter à Ganache")
        
        self.contract = None

    def load_contract(self, address, abi):
        """Charge le contrat déjà déployé"""
        self.contract = self.w3.eth.contract(address=address, abi=abi)

    def send_training_record(self, account_address, private_key, round_num, model_hash, accuracy, loss):
        """Envoie une transaction pour enregistrer un round"""
        # Conversion des floats en entiers pour Solidity
        acc_int = int(accuracy * config.ACCURACY_PRECISION)
        loss_int = int(loss * config.LOSS_PRECISION)

        # Préparation de la transaction
        nonce = self.w3.eth.get_transaction_count(account_address)
        
        txn = self.contract.functions.recordTraining(
            round_num,
            model_hash,
            acc_int,
            loss_int
        ).build_transaction({
            'chainId': self.w3.eth.chain_id,
            'gas': 500000,
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })

        # Signature et envoi
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Attendre la confirmation (reçu)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_client_history(self, client_address):
        """Lit l'historique depuis la blockchain"""
        return self.contract.functions.history(client_address).call()