from web3 import Web3
from pprint import pprint

# Connect to Ganache
URL = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(URL))

# Check if connected to Ganache
if not w3.is_connected():
    print("Failed to connect to Ganache")
    exit()

# John and Jack addresses and John's private key
john_addr = w3.eth.accounts[0]  # Account 1 (John)
jack_addr = w3.eth.accounts[1]  # Account 2 (Jack)
john_prik = 'b468f5d80bedce5afeaa3491161fd8ab55e9b03d71dee6374ca07b2a8c0ad3db'  # Replace with the actual private key for John

# Get the balance of an address in ether
def get_balance(addr):
    wei = w3.eth.get_balance(addr)
    ether = w3.from_wei(wei, 'ether')  # Convert from wei to ether (Ganache already works with ether)
 # Convert from wei to ether (Ganache already works with ether)
    return ether

# Get chainId, nonce, and gasPrice info for the raw transaction
def get_info():
    cid = w3.eth.chain_id
    nonce = w3.eth.get_transaction_count(john_addr)  # Get the nonce for the sender address
    block = w3.eth.get_block("latest")
    gas_price = w3.eth.gas_price  # Use gasLimit as a reference for gasPrice
    return cid, nonce, gas_price
print(get_info())

# Send the raw transaction
def send_raw_tx(sender_prik, value_in_wei, receiver_addr):
    cid, nonce, gas_price = get_info()
    
    balance = w3.eth.get_balance(john_addr)
    if balance < value_in_wei + (gas_price * 21000):  # 21000 is a reasonable gas limit for a transfer
        raise Exception("Insufficient funds for transaction and gas fee")
    
    # Construct the transaction
    tx = {
        'to': receiver_addr,
        'value': value_in_wei,  # Value in wei
        'nonce': nonce,
        'chainId': cid,  # Chain ID
        'gasPrice': gas_price,  # Gas price (in wei)
        'gas': 21000,  # Gas limit for simple transactions
    }
    
    # Sign the transaction with sender's private key
    signed_tx = w3.eth.account.sign_transaction(tx, sender_prik)
    
    # Send the raw transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

# Main execution: Send 2 ETH from John to Jack
def main():
    # Check the balance before the transaction
    print(f"John's balance before tx: {get_balance(john_addr)} ETH")
    print(f"Jack's balance before tx: {get_balance(jack_addr)} ETH")
    
    # 2 ETH in wei
    value_in_wei = w3.to_wei(2, 'ether')  # Convert ETH to wei (Ganache works with wei)

    # Send the raw transaction
    tx_hash = send_raw_tx(john_prik, value_in_wei, jack_addr)

    # Output the transaction hash
    print(f"Transaction Hash: {tx_hash}")
    
    # Check the balance after the transaction
    print(f"John's balance after tx: {get_balance(john_addr)} ETH")
    print(f"Jack's balance after tx: {get_balance(jack_addr)} ETH")

if __name__ == "__main__":
    main()
