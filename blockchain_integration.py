from web3 import Web3

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

def store_to_blockchain(content):
    hash_value = web3.keccak(text=content).hex()
    return hash_value
