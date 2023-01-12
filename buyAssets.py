import json
import time
import traceback
import requests
from web3 import Web3
import AccessToken
import GetAxieGenes512Custom
import txUtils
from assetTypes import axieFunctions
from assetTypes import itemFunctions
from assetTypes import landFunctions

if True:
    with open("config.json") as f:
        json_data = json.load(f)
        key = json_data['key']
        if key == "0xYOUR_PRIVATE_KEY":
            key = input("Please enter your private key")
        if json_data['address'] == "ronin:YOUR_RONIN_ADDRESS":
            json_data['address'] = input("Please enter your ronin address")
        if not Web3.is_address(json_data['address'].replace("ronin:", "0x")):
            print("Invalid address entered. Please try again. Both ronin: and 0x are accepted. Exiting.")
            raise SystemExit
        address = Web3.to_checksum_address(json_data['address'].replace("ronin:", "0x"))
        accessToken = AccessToken.GenerateAccessToken(key, address)
        if not str(type(json_data['gasPrice'])) == "<class 'int'>":
            print("Invalid gas price entered. Must be a whole number. Exiting.")
            raise SystemExit
        gasPrice = json_data['gasPrice']
    try:
        with open("filters.json") as f:
            filters = json.load(f)
    except:
        with open("filters.json", "w") as f:
            f.write(json.dumps({}))
        with open("filters.json") as f:
            filters = json.load(f)
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
        Web3.to_checksum_address('0xfff9ce5f71ca6178d3beecedb61e7eff1602950e'),
        115792089237316195423570985008687907853269984665640564039457584007913129639935
    ).build_transaction({
        'chainId': 2020,
        'gas': 481337,
        'gasPrice': Web3.to_wei(20, 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signed_txn = txUtils.w3.eth.account.sign_transaction(send_txn, private_key=key)
    sentTx = Web3.to_hex(Web3.keccak(signed_txn.rawTransaction))
    txUtils.sendTx(signed_txn)
    return sentTx


def fetchRecent(types, attempts=0):
    url = "https://graphql-gateway.axieinfinity.com/graphql?r=maxbrand99&query={"
    if "axies" in types:
        url += "axies(from:100,size:100,sort:Latest,auctionType:Sale,owner:null){total,results{id,class,stage,title,breedCount,bodyShape,newGenes,battleInfo{banned}order{...on%20Order{id,maker,kind,assets{...on%20Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}potentialPoints{beast,aquatic,plant,bug,bird,reptile,mech,dawn,dusk}}}"
    if "lands" in types:
        url += "lands(from:0,size:100,sort:Latest,auctionType:Sale,owner:null){total,results{tokenId,landType,order{...on%20Order{id,maker,kind,assets{...on%20Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}}}"
    if "items" in types:
        url += "items(from:0,size:100,sort:Latest,auctionType:Sale,owner:null){total,results{landType,rarity,tokenId,itemAlias,order{...on%20Order{id,maker,kind,assets{...on%20Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}}}"
    url += "}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken,
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
    }
    try:
        response = requests.request("GET", url, headers=headers)
    except:
        if attempts >= 3:
            print("fetchRecent request")
            print("Something is wrong.")
            print(traceback.format_exc())
            return {}
        print("Something failed with fetch recent request. Waiting 5 seconds.")
        time.sleep(5)
        return fetchRecent(types, attempts + 1)
    try:
        temp = json.loads(response.text)['data'][types[0]]['total']
        if temp:
            return json.loads(response.text)
    except:
        if attempts >= 3:
            print("fetchRecent")
            print("Something is wrong.")
            print("response:\t" + response.text)
            print(traceback.format_exc())
            return {}
        print("Something failed with fetch recent. Waiting 5 seconds.")
        time.sleep(5)
        return fetchRecent(types, attempts + 1)


def checkBugged(asset):
    order = asset['order']
    try:
        marketplaceContract.functions.interactWith(
            'ORDER_EXCHANGE',
            marketplaceContract.encodeABI(fn_name='orderValid', args=[
                order['hash'],
                [
                    Web3.to_checksum_address(order['maker']),
                    1,
                    [[
                        1,
                        Web3.to_checksum_address(order['assets'][0]['address']),
                        int(order['assets'][0]['id']),
                        int(order['assets'][0]['quantity'])
                    ]],
                    int(order['expiredAt']),
                    Web3.to_checksum_address("0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5"),
                    int(order['startedAt']),
                    int(order['basePrice']),
                    int(order['endedAt']),
                    int(order['endedPrice']),
                    0,
                    int(order['nonce']),
                    425
                ]
            ])
        ).call()
        return False
    except:
        return True


def buyAsset(asset):
    order = asset['order']
    marketTx = marketplaceContract.functions.interactWith(
        'ORDER_EXCHANGE',
        marketplaceContract.encodeABI(fn_name='settleOrder', args=[
            0,
            int(order['currentPrice']),
            Web3.to_checksum_address("0xa8Da6b8948D011f063aF3aA8B6bEb417f75d1194"),
            order['signature'],
            [
                Web3.to_checksum_address(order['maker']),
                1,
                [[
                    1,
                    Web3.to_checksum_address(order['assets'][0]['address']),
                    int(order['assets'][0]['id']),
                    int(order['assets'][0]['quantity'])
                ]],
                int(order['expiredAt']),
                Web3.to_checksum_address("0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5"),
                int(order['startedAt']),
                int(order['basePrice']),
                int(order['endedAt']),
                int(order['endedPrice']),
                0,
                int(order['nonce']),
                425
            ]
        ])
    ).build_transaction({
        'chainId': 2020,
        'gas': 481337,
        'gasPrice': Web3.to_wei(int(gasPrice), 'gwei'),
        'nonce': txUtils.getNonce(address)
    })
    signedTx = txUtils.w3.eth.account.sign_transaction(marketTx, private_key=key)
    return signedTx


def checkAxie(axie):
    if axie is None:
        return False
    if axie['order'] is None:
        return False
    for filterName in filters:
        if not filters[filterName]["type"] == "axies":
            continue
        myPrice = Web3.to_wei(filters[filterName]['price'], 'ether')
        if myPrice >= int(axie['order']['currentPrice']):
            if int(axie['order']['endedPrice']) == 0 and int(axie['order']['endedAt']) == 0:
                priceChange = 0
            else:
                priceChange = (int(axie['order']['endedPrice']) - int(axie['order']['basePrice'])) / int(axie['order']['duration'])
            # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
            # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
            # i doubt it will ever take 10s, but would rather be safe.
            # feel free to change the 10 to something less if you want to (at your own risk)
            if int(axie['order']['currentPrice']) + (priceChange * 10) > myPrice:
                print(f"not buying {axie['id']}, someone is doing something funky.")
                continue
        else:
            continue

        if filters[filterName]['num'] <= 0:
            continue

        myFilter = filters[filterName]['filter']

        if 'classes' in myFilter:
            axieClass = axie['class']
            if not axieClass in myFilter['classes']:
                continue
        if 'bodyShapes' in myFilter:
            axieBody = axie['bodyShape']
            if not axieBody in myFilter['bodyShapes']:
                continue
        if 'title' in myFilter:
            axieTitle = axie['title']
            if not axieTitle in myFilter['title']:
                continue
        if 'breedCount' in myFilter:
            axieBreeds = axie['breedCount']
            if axieBreeds < myFilter['breedCount'][0] or axieBreeds > myFilter['breedCount'][1]:
                continue

        filterSpecial = {}
        filterPotential = {}
        parts = {}
        ignoreParts = {}
        parseGenes = False
        for value in myFilter:
            if value.startswith("num"):
                filterSpecial[value.replace("num", "").lower()] = myFilter[value][0]
                parseGenes = True
            elif value.startswith("pp"):
                filterPotential[value.replace("pp", "").lower()] = myFilter[value][0]
            elif value == "parts":
                parseGenes = True
                for part in myFilter['parts']:
                    if part[0] == "!":
                        part = part.replace("!", "")
                        temp = part.split("-")
                        if not temp[0] in ignoreParts:
                            ignoreParts[temp[0]] = []
                        ignoreParts[temp[0]].append(part)
                    else:
                        temp = part.split("-")
                        if not temp[0] in parts:
                            parts[temp[0]] = []
                        parts[temp[0]].append(part)
            elif value in ["pureness", "purity"]:
                parseGenes = True

        if not filterPotential == {}:
            axiePotential = axie['potentialPoints']
            potentialMatch = True
            for axieClass in filterPotential:
                if not axiePotential[axieClass] == filterPotential[axieClass]:
                    potentialMatch = False
                    break
            if not potentialMatch:
                continue

        if parseGenes:
            axieSpecial = {
                "mystic": 0,
                "japan": 0,
                "xmas": 0,
                "summer": 0,
                "shiny": 0
            }
            purity = 0.0
            pureness = {}
            genes = json.loads(GetAxieGenes512Custom.getAxieGeneImage512(axie['newGenes']))
            hasParts = True
            for part in genes:
                if not genes[part]['d']['class'] in pureness:
                    pureness[genes[part]['d']['class']] = 0
                pureness[genes[part]['d']['class']] += 1
                if part in parts:
                    if not genes[part]['d']['partId'] in parts[part]:
                        hasParts = False
                if part in ignoreParts:
                    if genes[part]['d']['partId'] in ignoreParts[part]:
                        hasParts = False
                if genes[part]['d']['specialGenes'] is not None:
                    axieSpecial[genes[part]['d']['specialGenes']] += 1
                if genes[part]['d']['class'] == axie['class'].lower():
                    purity += 0.375
                if genes[part]['r1']['class'] == axie['class'].lower():
                    purity += 0.09375
                if genes[part]['r2']['class'] == axie['class'].lower():
                    purity += 0.03125
            purity = round((purity / 3.0) * 100)
            if 'pureness' in myFilter:
                myPureness = 0
                for axieClass in pureness:
                    if pureness[axieClass] > myPureness:
                        myPureness = pureness[axieClass]
                if not myPureness >= int(myFilter['pureness'][0]):
                    continue
            if 'purity' in myFilter:
                if not purity >= int(myFilter['purity'][0]):
                    continue
            if 'parts' in myFilter:
                if not hasParts:
                    continue
            if not filterSpecial == {}:
                specialMatch = True
                for special in filterSpecial:
                    if not axieSpecial[special] in filterSpecial[special]:
                        specialMatch = False
                        break
                if not specialMatch:
                    continue
        return filterName
    return False


def checkLand(land):
    if land is None:
        return False
    if land['order'] is None:
        return False
    for filterName in filters:
        if not filters[filterName]["type"] == "lands":
            continue
        myPrice = Web3.to_wei(filters[filterName]['price'], 'ether')
        if myPrice >= int(land['order']['currentPrice']):
            if int(land['order']['endedPrice']) == 0 and int(land['order']['endedAt']) == 0:
                priceChange = 0
            else:
                priceChange = (int(land['order']['endedPrice']) - int(land['order']['basePrice'])) / int(land['order']['duration'])
            # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
            # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
            # i doubt it will ever take 10s, but would rather be safe.
            # feel free to change the 10 to something less if you want to (at your own risk)
            if int(land['order']['currentPrice']) + (priceChange * 10) > myPrice:
                print(f"not buying {land['tokenId']}, someone is doing something funky.")
                continue
        else:
            continue

        if filters[filterName]['num'] <= 0:
            continue

        myFilter = filters[filterName]['filter']

        if 'landType' in myFilter:
            landType = land['landType']
            if not landType in myFilter['landType']:
                continue


        return filterName
    return False


def checkItem(item):
    if item is None:
        return False
    if item['order'] is None:
        return False
    for filterName in filters:
        if not filters[filterName]["type"] == "items":
            continue
        myPrice = Web3.to_wei(filters[filterName]['price'], 'ether')
        if myPrice >= int(item['order']['currentPrice']):
            if int(item['order']['endedPrice']) == 0 and int(item['order']['endedAt']) == 0:
                priceChange = 0
            else:
                priceChange = (int(item['order']['endedPrice']) - int(item['order']['basePrice'])) / int(item['order']['duration'])
            # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
            # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
            # i doubt it will ever take 10s, but would rather be safe.
            # feel free to change the 10 to something less if you want to (at your own risk)
            if int(item['order']['currentPrice']) + (priceChange * 10) > myPrice:
                print(f"not buying {item['tokenId']}, someone is doing something funky.")
                continue
        else:
            continue

        if filters[filterName]['num'] <= 0:
            continue

        myFilter = filters[filterName]['filter']

        if 'landType' in myFilter:
            landType = item['landType']
            if not landType in myFilter['landType']:
                continue
        if 'rarity' in myFilter:
            itemRarity = item['rarity']
            if not itemRarity in myFilter['rarity']:
                continue
        if 'itemAlias' in myFilter:
            itemAlias = item['itemAlias']
            if not itemAlias in myFilter['itemAlias']:
                continue
        return filterName
    return False


def runLoop():
    txs = []
    attemptedAssets = []
    checkedAssets = []
    attemptedTxs = {}
    count = 0
    balance = ethContract.functions.balanceOf(address).call()
    purchasedAssets = 0
    assetTypes = []
    for filterName in filters:
        assetType = filters[filterName]['type']
        if not assetType in assetTypes:
            assetTypes.append(assetType)
    startTime = time.time()
    while True:
        amountToSpend = 0
        market = fetchRecent(assetTypes)
        if market == {}:
            print("Failed to fetch recent. Axie servers might be having issues. Waiting 60 seconds.")
            time.sleep(60)
            continue
        for assetType in assetTypes:
            for asset in market['data'][assetType]['results']:
                if 'id' in asset:
                    if asset['id'] in attemptedAssets:
                        continue
                    if asset['id'] in checkedAssets:
                        continue
                    checkedAssets.append(asset['id'])
                else:
                    if asset['tokenId'] in attemptedAssets:
                        continue
                    if asset['tokenId'] in checkedAssets:
                        continue
                    checkedAssets.append(asset['tokenId'])
                try:
                    if assetType == "axies":
                        if asset['battleInfo']['banned']:
                            continue
                        if not asset['stage'] == 4:
                            continue
                        filterName = checkAxie(asset)
                    elif assetType == "lands":
                        filterName = checkLand(asset)
                    elif assetType == "items":
                        filterName = checkItem(asset)
                    else:
                        print("Filter did match any of the availible types, something is wrong.")
                        raise SystemExit
                except:
                    print(asset)
                    print(traceback.format_exc())
                    raise SystemExit
                if filterName:
                    amountToSpend += int(asset['order']['currentPrice'])
                    if amountToSpend > balance:
                        break

                    filters[filterName]['num'] -= 1
                    tx = buyAsset(asset)
                    txs.append(tx)
                    if 'id' in asset:
                        print(f"Attempting to buy Asset #{asset['id']} with filter {filterName}.")
                        attemptedTxs[Web3.to_hex(Web3.keccak(tx.rawTransaction))] = {'asset': asset['id'], 'name': filterName}
                        attemptedAssets.append(asset['id'])
                    else:
                        print(f"Attempting to buy Asset #{asset['tokenId']} with filter {filterName}.")
                        attemptedTxs[Web3.to_hex(Web3.keccak(tx.rawTransaction))] = {'asset': asset['tokenId'], 'name': filterName}
                        attemptedAssets.append(asset['tokenId'])
        if len(txs) > 0:
            txUtils.sendTxThreads(txs)
            for tx in txs:
                sentTx = Web3.to_hex(Web3.keccak(tx.rawTransaction))
                receipt = txUtils.w3.eth.get_transaction_receipt(sentTx)
                if not receipt.status == 1:
                    purchasedAssets -= 1
                    filters[attemptedTxs[sentTx]['name']]['num'] += 1
                    print(f"Buying asset {attemptedTxs[sentTx]['asset']} failed with filter {attemptedTxs[sentTx]['name']}.")
                else:
                    purchasedAssets += 1
                    print(f"Buying asset {attemptedTxs[sentTx]['asset']} succeded with filter {attemptedTxs[sentTx]['name']}.")
            txs = []
            with open("filters.json", "w") as f:
                f.write(json.dumps(filters))
            buyMore = False
            affordMore = False
            cheapestFilter = Web3.to_wei(99999, "ether")
            balance = ethContract.functions.balanceOf(address).call()
            for filterName in filters:
                if filters[filterName]['num'] > 0:
                    buyMore = True
                myPrice = Web3.to_wei(filters[filterName]['price'], 'ether')
                if myPrice < balance:
                    affordMore = True
                if myPrice < cheapestFilter:
                    cheapestFilter = myPrice
            if not buyMore:
                print(f"Bought {purchasedAssets} assets. No filters have any assets left. Exiting.")
                raise SystemExit
            if not affordMore:
                print(f"You do not have enough ETH to buy anything. Current cheapest filter price you have set is {cheapestFilter / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting.")
                raise SystemExit
        count += 1
        if count % 120 == 0:
            # print("Still waiting. Printing this so you know I am still alive.")
            endTime = time.time()
            print(f"Finished 120 Loops. Total time: {endTime - startTime}. Time per loop: {(endTime - startTime)/120}")
            startTime = time.time()
        if len(checkedAssets) >= 10000:
            checkedAssets = []

        time.sleep(1)


def init():
    if filters == {}:
        print("You must create at least 1 filter.")
        return mainMenu()
    ronBalance = txUtils.w3.eth.get_balance(address)
    if ronBalance < (481337 * Web3.to_wei(int(gasPrice), 'gwei')):
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
            print(f"Approved at tx: {sentTx}")

    cheapestFilter = Web3.to_wei(99999, "ether")
    affordMore = False
    balance = ethContract.functions.balanceOf(address).call()
    for filterName in filters:
        myPrice = Web3.to_wei(filters[filterName]['price'], 'ether')
        if myPrice < balance:
            affordMore = True
        if myPrice < cheapestFilter:
            cheapestFilter = myPrice
    if not affordMore:
        print(f"You do not have enough ETH to buy anything. Current cheapest filter price you have set is {cheapestFilter / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting.")
        raise SystemExit

    filterNames = list(filters.keys())
    print("Checking markets. This might take a few minutes, please be patient.")
    for filterName in filterNames:
        # this check is for current assets on the marketplace.
        # if there are 1 or more assets under the price you have set, it will ask you if you want to continue.
        myFilter = filters[filterName]['filter']
        price = Web3.to_wei(filters[filterName]['price'], 'ether')
        assetType = filters[filterName]['type']
        if assetType == "axies":
            market = axieFunctions.fetchMarket(accessToken, myFilter)
        elif assetType == "lands":
            market = landFunctions.fetchMarket(accessToken, myFilter)
        elif assetType == "items":
            market = itemFunctions.fetchMarket(accessToken, myFilter)
        else:
            print("Filter did match any of the availible types, something is wrong.")
            raise SystemExit
        cheapest = Web3.to_wei(99999, "ether")
        count = 0
        for asset in market['data'][assetType]['results']:
            if checkBugged(asset):
                continue
            if price >= int(asset['order']['currentPrice']):
                count += 1
            if int(asset['order']['currentPrice']) < cheapest:
                cheapest = int(asset['order']['currentPrice'])
        if count > 0:
            print(f"There are at least {count} assets that are less than the price you have set in the filter {filterName}.")
            print(f"Current cheapest asset is {cheapest / (10 ** 18)} ETH and your buy price is {price / (10 ** 18)} ETH.")
            myInput = input("Would you like to remove this filter? Saying no, will send you back to main menu where you can edit it. (Y/N)\n").lower()
            if not myInput == "y":
                print("You have chosen not to continue. Choose option 2 from the main menu to edit your filter.")
                return mainMenu()
            else:
                print("Deleting filter " + filterName + ".")
                del filters[filterName]
                with open("filters.json", "w") as f:
                    f.write(json.dumps(filters))
                print("Checking the remaining filters.")
        time.sleep(1)

    print("Starting loop.")
    runLoop()


def createFilter(filterName="", purchasePrice=0, newFilter=None, numAssets=0, assetType="", skipCreate=False):
    if filterName == "":
        filterName = input("Please enter a name for your filter. Or leave blank to go back to main menu.\n")
        if filterName in filters:
            print("This filter name already exists. If you want to edit a current filter, please go back to the main menu and choose option 2.")
            return createFilter(purchasePrice=purchasePrice, newFilter=newFilter, numAssets=numAssets, assetType=assetType, skipCreate=skipCreate)
        if filterName == "":
            return mainMenu()
    if purchasePrice == 0:
        purchasePrice = input("Please enter the purchase price of assets for this filter.\n")
        try:
            purchasePrice = float(purchasePrice)
        except:
            print("Purchase price is invalid. Please only enter a number.")
            return createFilter(filterName=filterName, newFilter=newFilter, numAssets=numAssets, assetType=assetType, skipCreate=skipCreate)
    if numAssets == 0:
        numAssets = input("Please enter the number of assets to buy with this filter.\n")
        try:
            numAssets = int(numAssets)
        except:
            print("Num assets is invalid. Please only enter a number.")
            return createFilter(filterName=filterName, purchasePrice=purchasePrice, newFilter=newFilter, assetType=assetType, skipCreate=skipCreate)
    if newFilter is None:
        newFilter = {}
        url = input("Please paste full marketplace URL\n")
        if assetType == "":
            assetType = url[:url.find("?")].replace("https://app.axieinfinity.com/marketplace/", "").replace("/", "")
        elif not assetType == url[:url.find("?")].replace("https://app.axieinfinity.com/marketplace/", "").replace("/", ""):
            newAssetType = url[:url.find("?")].replace("https://app.axieinfinity.com/marketplace/", "").replace("/", "")
            print("Cannot change filter type. Previous type was " + assetType + " new filter type is " + newAssetType + ".")
            return createFilter(filterName=filterName, purchasePrice=purchasePrice, numAssets=numAssets, assetType=assetType, skipCreate=skipCreate)
        try:
            inputData = url[url.find("?") + 1:].split("&")
            for value in inputData:
                tempData = value.split("=")
                filterType = tempData[0]
                try:
                    filterValue = int(tempData[1])
                except:
                    filterValue = tempData[1]
                if filterType in ["auctionTypes", "stage", "page", "partTypes", "specialCollection"]:
                    continue
                if filterType in ["numMystic", "numJapan", "numXmas", "numShiny", "numSummer"]:
                    if filterType in newFilter:
                        if filterValue < newFilter[filterType][0]:
                            inc = -1
                        else:
                            inc = 1
                        for i in range(newFilter[filterType][0]+inc, filterValue, inc):
                            newFilter[filterType].append(i)
                if filterType == "excludeParts":
                    filterType = "parts"
                    if filterType in newFilter and filterValue in newFilter['parts']:
                        newFilter['parts'][newFilter['parts'].index(filterValue)] = "!" + filterValue
                        continue
                    else:
                        filterValue = "!" + filterValue
                if filterType == 'title':
                    filterValue = filterValue.replace("+", " ")
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
            # print(traceback.format_exc())
            return createFilter(filterName=filterName, purchasePrice=purchasePrice, numAssets=numAssets, skipCreate=skipCreate)

    if not skipCreate:
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
            choice = input("No assets exist with your filter. Are you sure you want to continue? (Y/N)\n")
            if not choice.lower() == "y":
                return createFilter()
        else:
            print(f"Found {num} assets that match your filter. Moving to next step.")

    filters[filterName] = {
        "price": purchasePrice,
        "filter": newFilter,
        "num": numAssets,
        "type": assetType
    }
    with open("./filters.json", "w") as f:
        f.write(json.dumps(filters))
    if not skipCreate:
        print("Filter created successfully.\n")
        return createFilter()
    else:
        print("Filter edited successfully.\n")
        return mainMenu()


def editFilter(filterName="", attempts=0):
    if filterName == "":
        count = 0
        filterNames = list(filters.keys())
        for filterName in filterNames:
            count += 1
            print(f"{count}. {filterName}")
        choice = input("Enter the number of the filter you would like to edit, or leave blank to go back to main menu.\n")
        if choice == "":
            return mainMenu()
        try:
            choice = int(choice)
            if not (0 < choice <= count):
                print("The filter you entered does not exist, please try again.")
                return editFilter()
        except:
            print("The filter you entered does not exist, please try again.")
            return editFilter()
        filterName = filterNames[int(choice)-1]

    print("1. Filter name")
    print("2. Filter price")
    print("3. Filter data")
    print("4. Filter numAssets")
    choice = input("What would you like to edit?\n")
    if not choice in ["1", "2", "3", "4"]:
        if attempts < 2:
            print("Invalid entry, please try again.")
            return editFilter(filterName, attempts + 1)
        else:
            print("Failed input 3 times. Returning to Main Menu.")
            return mainMenu()
    filterPrice = filters[filterName]['price']
    filterData = filters[filterName]['filter']
    filterNum = filters[filterName]['num']
    assetType = filters[filterName]['type']
    del filters[filterName]
    if choice == "1":
        return createFilter(purchasePrice=filterPrice, newFilter=filterData, numAssets=filterNum, assetType=assetType, skipCreate=True)
    elif choice == "2":
        return createFilter(filterName=filterName, newFilter=filterData, numAssets=filterNum, assetType=assetType, skipCreate=True)
    elif choice == "3":
        return createFilter(filterName=filterName, purchasePrice=filterPrice, numAssets=filterNum, skipCreate=True)
    elif choice == "4":
        return createFilter(filterName=filterName, purchasePrice=filterPrice, newFilter=filterData, assetType=assetType, skipCreate=True)
    return mainMenu()


def deleteFilter(filterName="", attempts=0):
    if filterName == "":
        count = 0
        filterNames = list(filters.keys())
        for filterName in filterNames:
            count += 1
            print(f"{count}. {filterName}")
        choice = input("Enter the number of the filter you would like to delete, or leave blank to go back to main menu.\n")
        if choice == "":
            return mainMenu()
        try:
            choice = int(choice)
            if not (0 < choice <= count):
                print("The filter you entered does not exist, please try again.")
                return deleteFilter()
        except:
            print("The filter you entered does not exist, please try again.")
            return deleteFilter()
        filterName = filterNames[int(choice) - 1]
    filterInput = input(f"Please enter the filter name \"{filterName}\" to confirm deleting this filter (case matters for this one), or leave blank to go back to main menu.\n")
    if filterInput == "":
        return mainMenu()
    if filterInput == filterName:
        del filters[filterName]
        with open("./filters.json", "w") as f:
            f.write(json.dumps(filters))
        print(f"Deleted filter {filterName}")
    else:
        if attempts < 2:
            print("Invalid entry, please try again.")
            return deleteFilter(filterName, attempts + 1)
        else:
            print("Failed input 3 times. Returning to Main Menu.")
            return mainMenu()

    return mainMenu()


def mainMenu(attempts=0):
    print("Main Menu")
    print("1. Create new filter")
    print("2. Edit existing filter")
    print("3. Delete existing filter")
    print("4. Run the script")
    print("5. Exit")
    choice = input("What would you like to do?\n")
    if not choice in ["1", "2", "3", "4", "5"]:
        if attempts < 2:
            print("Invalid entry, please try again.")
            return mainMenu(attempts + 1)
        else:
            print("Failed input 3 times. Exiting.")
            raise SystemExit
    if choice == "1":
        return createFilter()
    elif choice == "2":
        return editFilter()
    elif choice == "3":
        return deleteFilter()
    elif choice == "4":
        return init()
    elif choice == "5":
        raise SystemExit
    else:
        return mainMenu(attempts + 1)


mainMenu()
