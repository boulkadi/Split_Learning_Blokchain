from web3 import Web3

RPC_URL = "http://127.0.0.1:7545"  # Ganache local
w3 = Web3(Web3.HTTPProvider(RPC_URL))

print("Connecté :", w3.is_connected())
print("Dernier bloc :", w3.eth.block_number)

# Compte Ganache
account = w3.eth.accounts[0]
print("Compte utilisé :", account)
