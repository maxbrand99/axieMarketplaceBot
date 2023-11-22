# Author: Maxbrand99

from eth_account.messages import encode_defunct
from web3 import Web3
import traceback
import json
import requests

def GenerateAccessToken(key, address, attempts=0):
    def getNonce(attempts2=0):
        try:
            url = f"https://athena.skymavis.com/v2/public/auth/ronin/fetch-nonce?address={address}"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
            }
            
            response = requests.request("GET", url, headers=headers)
            json_data = json.loads(response.text)
            return json_data
        except:
            if attempts2 > 3:
                print("Could not generate AccessToken Random Message. Are the servers having issues?")
                print(traceback.format_exc())
                return None
            else:
                return getNonce(attempts2 + 1)

    def signRoninMessage(message, key, attempts2=0):
        try:
            mes = encode_defunct(text=message)
            ronweb3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', request_kwargs={"headers": {"content-type": "application/json", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}}))
            sig = ronweb3.eth.account.sign_message(mes, private_key=key)
            signature = sig['signature'].hex()
            return signature
        except:
            if attempts2 > 3:
                print("Could not Sign Message. Are the servers having issues?")
                print(traceback.format_exc())
                return None
            else:
                return signRoninMessage(message, key, attempts2 + 1)

    def createAccessToken(message, signature, attempts2=0):
        try:
            url = "https://athena.skymavis.com/v2/public/auth/ronin/login"
            payload = {
                'signature': signature,
                'message': message
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            return json_data['accessToken']
        except:
            if attempts2 > 3:
                print("Could not Create Access Token. Are the servers having issues?")
                print(traceback.format_exc())
                return None
            else:
                return createAccessToken(message, signature, attempts2 + 1)

    try:
        data = getNonce()
        message = f"""app.axieinfinity.com wants you to sign in with your Ronin account:\n{address.replace('0x', 'ronin:').lower()}\n\nI accept the Terms of Use (https://axieinfinity.com/terms-of-use) and the Privacy Policy (https://axieinfinity.com/privacy-policy)\n\nURI: https://app.axieinfinity.com\nVersion: 1\nChain ID: 2020\nNonce: {data['nonce']}\nIssued At: {data['issued_at']}\nExpiration Time: {data['expiration_time']}\nNot Before: {data['not_before']}"""
        signature = signRoninMessage(message, key)
        token = createAccessToken(message, signature)
        return token
    except:
        if attempts > 3:
            print("Unable To generate Access Token. This is gernerally an internet issue or a server issue.")
            print(traceback.format_exc())
            return None
        else:
            return GenerateAccessToken(key, address, attempts + 1)
