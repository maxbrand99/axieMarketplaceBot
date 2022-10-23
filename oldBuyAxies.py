# Author: Maxbrand99
import json
import time
import traceback
import requests
from web3 import Web3
import AccessToken
import txUtils

# DO NOT TOUCH ANYTHING IN THIS FILE OR YOU WILL BREAK IT.
if True:
    with open("filter.json") as f:
        myFilter = json.load(f)
    with open("config.json") as f:
        json_data = json.load(f)
        key = json_data['key']
        if key == "0xYOUR_PRIVATE_KEY":
            key = input("Please enter your private key")
        if json_data['address'] == "ronin:YOUR_RONIN_ADDRESS":
            json_data['address'] = input("Please enter your ronin address")
        if not Web3.isAddress(json_data['address'].replace("ronin:", "0x")):
            print("Invalid address entered. Please try again. Both ronin: and 0x are accepted. Exiting.")
            raise SystemExit
        address = Web3.toChecksumAddress(json_data['address'].replace("ronin:", "0x"))
        accessToken = AccessToken.GenerateAccessToken(key, address)
        if not (str(type(json_data['buyPrice'])) == "<class 'float'>" or str(
                type(json_data['buyPrice'])) == "<class 'int'>"):
            print("Invalid buy price entered. Must be a number (either decimal or whole number). Exiting.")
            raise SystemExit
        price = Web3.toWei(json_data['buyPrice'], 'ether')
        if not str(type(json_data['gasPrice'])) == "<class 'int'>":
            print("Invalid gas price entered. Must be a whole number. Exiting.")
            raise SystemExit
        gasPrice = json_data['gasPrice']
        if not str(type(json_data['numAxies'])) == "<class 'int'>":
            print("Invalid num axies entered. Must be a whole number. Exiting.")
            raise SystemExit
        numAxies = json_data['numAxies']
    ethContract = txUtils.eth()
    marketplaceContract = txUtils.marketplace()


# THIS IS FOR APPROVING ETH TO BE SPENT BY THE MARKETPLACE.
# WHEN YOU MAKE A NEW ACCOUNT ON MARKETPLACE, IT DOES THE SAME THING.
# The address being approved is 0xfff9ce5f71ca6178d3beecedb61e7eff1602950e which is Contract: Marketplace Gateway V2
# https://explorer.roninchain.com/address/ronin:fff9ce5f71ca6178d3beecedb61e7eff1602950e
# The amount approved is 115792089237316195423570985008687907853269984665640564039457584007913129639935
# This is the same amount that the ronin wallet approves.
def approve():
    send_txn = ethContract.functions.approve(
        Web3.toChecksumAddress('0xfff9ce5f71ca6178d3beecedb61e7eff1602950e'),
        115792089237316195423570985008687907853269984665640564039457584007913129639935
    ).buildTransaction({
        'chainId': 2020,
        'gas': 391337,
        'gasPrice': Web3.toWei(1, 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signed_txn = txUtils.w3.eth.account.sign_transaction(send_txn, private_key=key)
    sentTx = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
    txUtils.sendTx(signed_txn)
    return sentTx


def fetchMarket(attempts=0):
    url = "https://graphql-gateway.axieinfinity.com/graphql?r=maxbrand99"

    payload = {
        "query": "query GetAxieBriefList($auctionType:AuctionType,$criteria:AxieSearchCriteria,$from:Int,$sort:SortBy,$size:Int,$owner:String){axies(auctionType:$auctionType,criteria:$criteria,from:$from,sort:$sort,size:$size,owner:$owner){total,results{id,stage,class,breedCount,title,newGenes,bodyShape,battleInfo{banned}order{... on Order {id,maker,kind,assets{... on Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}potentialPoints{beast,aquatic,plant,bug,bird,reptile,mech,dawn,dusk}}}}",
        "variables": {
            "from": 0,
            "size": 100,
            "sort": "PriceAsc",
            "auctionType": "Sale",
            "owner": None,
            "criteria": myFilter
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken,
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    try:
        temp = json.loads(response.text)['data']['axies']['total']
        if temp:
            return json.loads(response.text)
    except:
        if attempts >= 3:
            print("fetchMarket")
            print("something is wrong. exiting the program.")
            print("filter:\t" + json.dumps(myFilter))
            print("response:\t" + response.text)
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(attempts+1)


def buyAxie(axie):
    order = axie['order']
    marketTx = marketplaceContract.functions.interactWith(
        'ORDER_EXCHANGE',
        marketplaceContract.encodeABI(fn_name='settleOrder', args=[
            0,
            int(order['currentPrice']),
            Web3.toChecksumAddress("0xa8Da6b8948D011f063aF3aA8B6bEb417f75d1194"),
            order['signature'],
            [
                Web3.toChecksumAddress(order['maker']),
                1,
                [[
                    1,
                    Web3.toChecksumAddress(order['assets'][0]['address']),
                    int(order['assets'][0]['id']),
                    int(order['assets'][0]['quantity'])
                ]],
                int(order['expiredAt']),
                Web3.toChecksumAddress("0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5"),
                int(order['startedAt']),
                int(order['basePrice']),
                int(order['endedAt']),
                int(order['endedPrice']),
                0,
                int(order['nonce']),
                425
            ]
        ])
    ).buildTransaction({
        'chainId': 2020,
        'gas': 391337,
        'gasPrice': Web3.toWei(int(gasPrice), 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signedTx = txUtils.w3.eth.account.sign_transaction(marketTx, private_key=key)
    return signedTx


def runLoop():
    txs = []
    attemptedAxies = []
    attemptedTxs = {}
    count = 0
    numToBuy = numAxies
    balance = ethContract.functions.balanceOf(address).call()
    while True:
        amountToSpend = 0
        market = fetchMarket()
        for axie in market['data']['axies']['results']:
            if axie['id'] in attemptedAxies:
                continue
            if price >= int(axie['order']['currentPrice']):
                if int(axie['order']['endedPrice']) == 0 and int(axie['order']['endedAt']) == 0:
                    priceChange = 0
                else:
                    priceChange = abs(int(axie['order']['basePrice']) - int(axie['order']['endedPrice'])) / int(
                        axie['order']['duration'])
                # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
                # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
                # i doubt it will ever take 10s, but would rather be safe.
                # feel free to change the 10 to something less if you want to (at your own risk)
                if int(axie['order']['currentPrice']) + (priceChange * 10) > price:
                    print("not buying " + str(axie['id']) + ", someone is doing something funky.")
                    continue

                amountToSpend += int(axie['order']['currentPrice'])
                if amountToSpend > balance:
                    break
                print("Attempting to buy Axie #" + str(axie['id']))
                tx = buyAxie(axie)
                txs.append(tx)
                attemptedTxs[Web3.toHex(Web3.keccak(tx.rawTransaction))] = axie['id']
                attemptedAxies.append(axie['id'])
                numToBuy -= 1
                if numToBuy <= 0:
                    break
        if len(txs) > 0:
            txUtils.sendTxThreads(txs)
            for tx in txs:
                sentTx = Web3.toHex(Web3.keccak(tx.rawTransaction))
                receipt = txUtils.w3.eth.get_transaction_receipt(sentTx)
                if not receipt.status == 1:
                    numToBuy += 1
                    print("Buying axie " + str(attemptedTxs[sentTx]) + " failed.")
                else:
                    print("Buying axie " + str(attemptedTxs[sentTx]) + " succeded.")
            txs = []
        if numToBuy <= 0:
            print("Bought " + str(numAxies) + " axies. This is the limit. Exiting.")
            raise SystemExit
        balance = ethContract.functions.balanceOf(address).call()
        if balance <= price:
            print("You do not have enough ETH to buy anything. Current price you have set is " + str(price / (10 ** 18)) + " ETH and you only have " + str(balance / (10 ** 18)) + " ETH. Exiting.")
            raise SystemExit
        count += 1
        if count % 100 == 0:
            print("Still waiting. Printing this so you know I am still alive.")
        time.sleep(1)


def checkFilter(attempts=0):
    url = "https://graphql-gateway.axieinfinity.com/graphql?r=maxbrand99"

    payload = {
        "query": "query GetAxieBriefList($auctionType:AuctionType,$criteria:AxieSearchCriteria,$from:Int,$sort:SortBy,$size:Int,$owner:String){axies(auctionType:$auctionType,criteria:$criteria,from:$from,sort:$sort,size:$size,owner:$owner){total}}",
        "variables": {
            "from": 0,
            "size": 0,
            "sort": "PriceAsc",
            "auctionType": "All",
            "owner": None,
            "criteria": myFilter
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken,
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    try:
        return json.loads(response.text)['data']['axies']['total']
    except:
        if attempts >= 3:
            print("fetchMarket")
            print("something is wrong. exiting the program.")
            print("filter:\t" + json.dumps(myFilter))
            print("response:\t" + str(response.text))
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(attempts + 1)


def init():
    # this check is to make sure that axies with your filter exist. This checks all axies listed or not listed.
    num = checkFilter()
    if num == 0:
        print("No axies exist with your filter. Please enter a new filter and try again. Exiting.")
        raise SystemExit
    else:
        print("Found " + str(num) + " axies that match your filter. Moving to next step.")

    # this check is for current axies on the marketplace.
    # if there are 1 or more axies under the price you have set, it will ask you if you want to continue.
    market = fetchMarket()
    cheapest = Web3.toWei(99999, "ether")
    count = 0
    for axie in market['data']['axies']['results']:
        if price >= int(axie['order']['currentPrice']):
            count += 1
        if int(axie['order']['currentPrice']) < cheapest:
            cheapest = int(axie['order']['currentPrice'])
    if count > 0:
        print("There are at least " + str(count) + " axies that are less than the price you have set in the filter.")
        print("Current cheapest axie is " + str(cheapest / (10 ** 18)) + " ETH and your buy price is " + str(price / (10 ** 18)) + " ETH.")
        print("If you continue, it will start sweeping all axies under the set price.")
        myInput = input("Would you like to continue? (Y/N)\n").lower()
        if not myInput == "y":
            print("You have chosen not to continue. Exiting.")
            raise SystemExit
        else:
            print("Moving to next step.")

    balance = ethContract.functions.balanceOf(address).call()
    if balance < price:
        print("You do not have enough ETH to buy anything. Current price you have set is " + str(price / (10 ** 18)) + " ETH and you only have " + str(balance / (10 ** 18)) + " ETH. Exiting.")
        raise SystemExit

    ronBalance = txUtils.w3.eth.getBalance(address)
    if ronBalance < (391337 * Web3.toWei(int(gasPrice), 'gwei')):
        print("You do not have enough RON for the entered gas price. Please lower gas price or add more RON.")
        raise SystemExit


    allowance = ethContract.functions.allowance(address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E").call()
    if allowance == 0:
        print("We need to approve eth for spending on the marketplace. Approving...")
        sentTx = approve()
        allowance = ethContract.functions.allowance(address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E").call()
        if allowance == 0:
            print("Something went wrong, approval didnt work. Exiting.")
            raise SystemExit
        else:
            print("Approved at tx: " + str(sentTx))

    print("Starting loop.")
    runLoop()


init()
