import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3
from . import config

def save_contract_info(address, abi, filename="contract_info.json"):
    """Sauvegarde l'adresse et l'ABI pour que les autres scripts les retrouvent."""
    data = {"address": address, "abi": abi}
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f" Infos du contrat sauvegardées dans {filename}")

def load_contract_info(filename="contract_info.json"):
    """Charge les données du contrat sans avoir à re-compiler."""
    if not os.path.exists(filename):
        return None, None
    with open(filename, "r") as f:
        data = json.load(f)
    return data["address"], data["abi"]

def deploy_registry(private_key, sender_address):
    # Installer et utiliser Solidity 0.8.0
    install_solc("0.8.0")
    
    # Chemin vers le contrat
    contract_path = "src/blockchain/blockchain_code/contracts/TrainingRegistry.sol"
    with open(contract_path, "r") as file:
        contract_source = file.read()

    # Compilation
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {"TrainingRegistry.sol": {"content": contract_source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}}
    }, solc_version="0.8.0")

    abi = compiled_sol["contracts"]["TrainingRegistry.sol"]["TrainingRegistry"]["abi"]
    bytecode = compiled_sol["contracts"]["TrainingRegistry.sol"]["TrainingRegistry"]["evm"]["bytecode"]["object"]

    w3 = Web3(Web3.HTTPProvider(config.GANACHE_URL))
    
    # Déploiement
    TrainingContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(sender_address)
    
    txn = TrainingContract.constructor().build_transaction({
        'chainId': w3.eth.chain_id, 
        'gas': 2000000, 
        'gasPrice': w3.to_wei('20', 'gwei'),
        'nonce': nonce
    })
    
    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # On sauvegarde les infos dès que le déploiement réussit
    save_contract_info(receipt.contractAddress, abi)

    return receipt.contractAddress, abi