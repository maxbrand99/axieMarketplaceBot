import requests
import json
import traceback


def fetchMarket(accessToken, myFilter, attempts=0):
    url = "https://graphql-gateway.axieinfinity.com/graphql?r=maxbrand99"

    payload = {
        "query": "query GetAxieBriefList($auctionType:AuctionType,$criteria:AxieSearchCriteria,$from:Int,$sort:SortBy,$size:Int,$owner:String){axies(auctionType:$auctionType,criteria:$criteria,from:$from,sort:$sort,size:$size,owner:$owner,){total,results{order{...on Order{id,maker,kind,assets{...on Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}}}}",
        "variables": {
            "from": 0,
            "size": 25,
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
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    except:
        if attempts >= 3:
            print("fetchMarket request")
            print("something is wrong. exiting the program.")
            print(traceback.format_exc())
            raise SystemExit
        return fetchMarket(accessToken, myFilter, attempts + 1)
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
        return fetchMarket(accessToken, myFilter, attempts + 1)


def checkFilter(accessToken, myFilter, attempts=0):
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
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    except:
        if attempts >= 3:
            print("checkFilter request")
            print("something is wrong. exiting the program.")
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(accessToken, myFilter, attempts + 1)
    try:
        return json.loads(response.text)['data']['axies']['total']
    except:
        if attempts >= 3:
            print("fetchAxieMarket")
            print("something is wrong. exiting the program.")
            print("filter:\t" + json.dumps(myFilter))
            print("response:\t" + response.text)
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(accessToken, myFilter, attempts + 1)
