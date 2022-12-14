# Author: Maxbrand99

import json
import requests
from eth_account.messages import encode_defunct
from web3 import Web3


def signRoninMessage(message, key, attempts2=0):
    try:
        mes = encode_defunct(text=message)
        ronweb3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc'))
        sig = ronweb3.eth.account.sign_message(mes, private_key=key)
        signature = sig['signature'].hex()
        return signature
    except Exception as e:
        if attempts2 > 3:
            print("Could not Sign Message. Are the servers having issues?")
            print(e)
            return None
        else:
            return signRoninMessage(message, key, attempts2 + 1)


def GenerateAccessToken(key, address, attempts=0):
    def getRandomMessage(attempts2=0):
        try:
            url = "https://graphql-gateway.axieinfinity.com/graphql"

            payload = '{"query":"mutation CreateRandomMessage{createRandomMessage}","variables":{}}'
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            return json_data['data']['createRandomMessage']
        except Exception as e:
            if attempts2 > 3:
                print("Could not generate AccessToken Random Message. Are the servers having issues?")
                print(e)
                return None
            else:
                return getRandomMessage(attempts2 + 1)

    def signRoninMessage(message, key, attempts2=0):
        try:
            mes = encode_defunct(text=message)
            ronweb3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc'))
            sig = ronweb3.eth.account.sign_message(mes, private_key=key)
            signature = sig['signature'].hex()
            return signature
        except Exception as e:
            if attempts2 > 3:
                print("Could not Sign Message. Are the servers having issues?")
                print(e)
                return None
            else:
                return signRoninMessage(message, key, attempts2 + 1)

    def CreateAccessToken(message, signature, address, attempts2=0):
        try:
            url = "https://graphql-gateway.axieinfinity.com/graphql"
            payload = '{"query":"mutation CreateAccessTokenWithSignature($input:SignatureInput!){createAccessTokenWithSignature(input:$input){newAccount,result,accessToken,__typename}}","variables":{"input":{"mainnet":"ronin","owner":"' + address + '","message":"' + message + '","signature":"' + signature + '"}}}'
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            return json_data['data']['createAccessTokenWithSignature']['accessToken']
        except Exception as e:
            if attempts2 > 3:
                print("Could not Create Access Token. Are the servers having issues?")
                print(e)
                return None
            else:
                return CreateAccessToken(message, signature, address, attempts2 + 1)

    try:
        myResponse = getRandomMessage()
        mySignature = signRoninMessage(myResponse, key)
        token = CreateAccessToken(repr(myResponse).replace("\'", ""), mySignature, address)
        return token
    except Exception as e:
        if attempts > 3:
            print(e)
            print("Unable To generate Access Token. This is gernerally an internet issue or a server issue.")
            return None
        else:
            return GenerateAccessToken(key, address, attempts + 1)
