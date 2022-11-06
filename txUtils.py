# Author: Maxbrand99

import concurrent.futures
import json
from web3 import Web3, exceptions

with open("abis.json") as file:
    w3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', request_kwargs={"headers":{"content-type":"application/json","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}}))
    # IF YOU HAVE YOUR OWN RPC URL, COMMENT OUT THE LINE ABOVE, UNCOMMENT THE LINE BELOW, AND ENTER IT ON THE LINE BELOW
    # w3 = Web3(Web3.HTTPProvider('http://mycustomrpc.com/rpc'))
    abis = json.load(file)
    nonces = {}


def eth():
    ethAbi = abis['eth']
    ethAddress = Web3.toChecksumAddress("0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5")
    ethContract = w3.eth.contract(address=ethAddress, abi=ethAbi)
    return ethContract


def marketplace():
    marketplaceAbi = abis['marketplace']
    marketplaceAddress = Web3.toChecksumAddress("0xfff9ce5f71ca6178d3beecedb61e7eff1602950e")
    marketplaceContract = w3.eth.contract(address=marketplaceAddress, abi=marketplaceAbi)
    return marketplaceContract


def sendTx(signedTxn, timeout=10):
    tx = signedTxn.hash
    try:
        w3.eth.send_raw_transaction(signedTxn.rawTransaction)
    except ValueError as e:
        print(e)
    tries = 0
    success = False
    while tries < 3:
        try:
            receipt = w3.eth.wait_for_transaction_receipt(tx, timeout)
            if receipt["status"] == 1:
                success = True
            break
        except (exceptions.TransactionNotFound, exceptions.TimeExhausted, ValueError):
            tries += 1
            print("Not found yet, waiting...")
    if success:
        return True
    return False


def getNonce(address):
    address = Web3.toChecksumAddress(address)
    nonce = w3.eth.get_transaction_count(address)
    if address in nonces:
        if nonces[address] < nonce:
            nonces[address] = nonce
        else:
            nonce = nonces[address]
    else:
        nonces[address] = nonce
    nonces[address] += 1
    return nonce


def sendTxThreads(txs, CONNECTIONS=100, TIMEOUT=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(sendTx, tx, TIMEOUT) for tx in txs)
        for future in concurrent.futures.as_completed(future_to_url):
            future.result()
