import json
import time
from web3 import Web3
import AccessToken
import txUtils
from assetTypes import axieFunctions
from assetTypes import itemFunctions
from assetTypes import landFunctions

# DO NOT TOUCH ANYTHING IN THIS FILE OR YOU WILL BREAK IT.
if True:
    try:
        with open("filter.json") as f:
            filterData = json.load(f)
    except:
        with open("filter.json", "w") as f:
            filterData = {
                "price": 0,
                "filter": {},
                "num": 0,
                "type": ""
            }
            f.write(json.dumps(filterData))
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
        if not str(type(json_data['gasPrice'])) == "<class 'int'>":
            print("Invalid gas price entered. Must be a whole number. Exiting.")
            raise SystemExit
        gasPrice = json_data['gasPrice']
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
        'gas': 481337,
        'gasPrice': Web3.toWei(1, 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signed_txn = txUtils.w3.eth.account.sign_transaction(send_txn, private_key=key)
    sentTx = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
    txUtils.sendTx(signed_txn)
    return sentTx


def buyAsset(asset):
    order = asset['order']
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
        'gas': 481337,
        'gasPrice': Web3.toWei(int(gasPrice), 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signedTx = txUtils.w3.eth.account.sign_transaction(marketTx, private_key=key)
    return signedTx


def runLoop(filterData):
    assetType = filterData['type']
    myFilter = filterData['filter']
    numAssets = filterData['num']
    price = Web3.toWei(filterData['price'], 'ether')
    txs = []
    attemptedAssets = []
    attemptedTxs = {}
    count = 0
    numToBuy = numAssets
    balance = ethContract.functions.balanceOf(address).call()
    while True:
        amountToSpend = 0
        if assetType == "axies":
            market = axieFunctions.fetchMarket(accessToken, myFilter)
        elif assetType == "lands":
            market = landFunctions.fetchMarket(accessToken, myFilter)
        elif assetType == "items":
            market = itemFunctions.fetchMarket(accessToken, myFilter)
        else:
            print("Filter did match any of the availible types, something is wrong.")
            raise SystemExit
        for asset in market['data'][assetType]['results']:
            if 'id' in asset and asset['id'] in attemptedAssets:
                continue
            elif 'tokenId' in asset and asset['tokenId'] in attemptedAssets:
                continue
            if price >= int(asset['order']['currentPrice']):
                if int(asset['order']['endedPrice']) == 0 and int(asset['order']['endedAt']) == 0:
                    priceChange = 0
                else:
                    priceChange = (int(asset['order']['endedPrice']) - int(asset['order']['basePrice'])) / int(
                        asset['order']['duration'])
                # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
                # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
                # i doubt it will ever take 10s, but would rather be safe.
                # feel free to change the 10 to something less if you want to (at your own risk)
                if int(asset['order']['currentPrice']) + (priceChange * 10) > price:
                    if 'id' in asset:
                        print(f"not buying {asset['id']}, someone is doing something funky.")
                    else:
                        print(f"not buying {asset['tokenId']}, someone is doing something funky.")
                    continue

                amountToSpend += int(asset['order']['currentPrice'])
                if amountToSpend > balance:
                    break
                tx = buyAsset(asset)
                txs.append(tx)
                if 'id' in asset:
                    print(f"Attempting to buy Asset #{asset['id']}.")
                    attemptedTxs[Web3.toHex(Web3.keccak(tx.rawTransaction))] = asset['id']
                    attemptedAssets.append(asset['id'])
                else:
                    print(f"Attempting to buy Asset #{asset['tokenId']}.")
                    attemptedTxs[Web3.toHex(Web3.keccak(tx.rawTransaction))] = asset['tokenId']
                    attemptedAssets.append(asset['tokenId'])
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
                    print(f"Buying asset {attemptedTxs[sentTx]} failed.")
                else:
                    print(f"Buying asset {attemptedTxs[sentTx]} succeded.")
            txs = []
        if numToBuy <= 0:
            print(f"Bought {numAssets} assets. This is the limit. Exiting.")
            raise SystemExit
        balance = ethContract.functions.balanceOf(address).call()
        if balance <= price:
            print(f"You do not have enough ETH to buy anything. Current price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting.")
            raise SystemExit
        count += 1
        if count % 120 == 0:
            print("Still waiting. Printing this so you know I am still alive.")
        time.sleep(1)


def createFilter(purchasePrice=0, newFilter=None, numAssets=0, assetType=""):
    if purchasePrice == 0:
        purchasePrice = input("Please enter the purchase price of assets for this filter.\n")
        try:
            purchasePrice = float(purchasePrice)
        except:
            print("Purchase price is invalid. Please only enter a number.")
            return createFilter(newFilter=newFilter, numAssets=numAssets, assetType=assetType)
    if numAssets == 0:
        numAssets = input("Please enter the number of assets to buy with this filter.\n")
        try:
            numAssets = int(numAssets)
        except:
            print("Num assets is invalid. Please only enter a number.")
            return createFilter(purchasePrice=purchasePrice, newFilter=newFilter, assetType=assetType)
    if newFilter is None:
        newFilter = {}
        url = input("Please paste full marketplace URL\n")
        if assetType == "":
            assetType = url[:url.find("?")].replace("https://app.axieinfinity.com/marketplace/", "").replace("/", "")
        try:
            inputData = url[url.find("?") + 1:].split("&")
            for value in inputData:
                tempData = value.split("=")
                filterType = tempData[0]
                try:
                    filterValue = int(tempData[1])
                except:
                    filterValue = tempData[1]
                if filterType == "region":
                    newFilter["region"] = "japan"
                    continue
                if filterType in ["auctionTypes", "stage", "page"]:
                    continue
                if filterType == "excludeParts":
                    filterType = "parts"
                    if filterValue in newFilter['parts']:
                        newFilter['parts'][newFilter['parts'].index(filterValue)] = "!" + filterValue
                        continue
                if filterType in ["mystic", "japan", "xmas", "shiny", "summer"]:
                    filterType = "num" + filterType.capitalize()
                if filterType == "class":
                    filterType = "classes"
                if filterType in ["part", "bodyShape"]:
                    filterType = filterType + "s"
                if filterType == 'title':
                    filterValue = filterValue.replace("-", " ")
                if filterType == "type":
                    filterType = "landType"
                if not filterType in newFilter:
                    newFilter[filterType] = []
                newFilter[filterType].append(filterValue)
            for value in newFilter:
                if len(newFilter[value]) == 0:
                    newFilter[value] = None
        except:
            print("Something went wrong with the filter. Did you enter the URL correctly?")
            print("Ex: https://app.axieinfinity.com/marketplace/axies/?class=Beast&mystic=1&auctionTypes=Sale")
            print("Would search for a 1 part mystic beast")
            return createFilter(purchasePrice=purchasePrice, numAssets=numAssets)

    if assetType == "axies":
        num = axieFunctions.checkFilter(accessToken, newFilter)
    elif assetType == "lands":
        num = landFunctions.checkFilter(accessToken, newFilter)
    elif assetType == "items":
        num = itemFunctions.checkFilter(accessToken, newFilter)
    else:
        print("Filter did match any of the availible types, something is wrong.")
        raise SystemExit
    if num == 0:
        print("No axies exist with your filter. Please enter a new filter and try again.")
        return createFilter(purchasePrice=purchasePrice, numAssets=numAssets)
    else:
        print(f"Found {num} assets that match your filter. Moving to next step.")

    filterData = {
        "price": purchasePrice,
        "filter": newFilter,
        "num": numAssets,
        "type": assetType
    }
    with open("./filter.json", "w") as f:
        f.write(json.dumps(filterData))

    return filterData


def init(filterData):
    if filterData['type'] == "" or filterData['filter'] == {} or filterData['num'] == 0 or filterData['price'] == 0:
        filterData = createFilter()
    else:
        choice = input("Would you like to use the current filter? (Y/N)\n")
        if not choice.lower() == "y":
            filterData = createFilter()
    price = Web3.toWei(filterData['price'], 'ether')
    balance = ethContract.functions.balanceOf(address).call()
    if balance < price:
        print("You do not have enough ETH to buy anything. Current price you have set is " + str(price / (10 ** 18)) + " ETH and you only have " + str(balance / (10 ** 18)) + " ETH. Exiting.")
        raise SystemExit

    ronBalance = txUtils.w3.eth.getBalance(address)
    if ronBalance < (481337 * Web3.toWei(int(gasPrice), 'gwei')):
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
    runLoop(filterData)


init(filterData)
