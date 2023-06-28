import requests

# Define the asset pairs to compare
asset_pairs = [('ETH', 'DAI'), ('DAI', 'USDC'), ('ETH', 'USDC')]

# Define the APIs for each platform
oneinch_api = 'https://api.1inch.exchange/v3.0/1/quote'
uniswap_api = 'https://api.uniswap.info/v2/ticker'
paraswap_api = 'https://apiv4.paraswap.io/v2/prices'


# Define a function to get the price of an asset pair from 1inch
def get_1inch_price(base, quote):
    params = {'fromTokenAddress': base, 'toTokenAddress': quote, 'amount': 1}
    response = requests.get(oneinch_api, params=params)
    return float(response.json()['toTokenAmount']) / float(response.json()['fromTokenAmount'])


# Define a function to get the price of an asset pair from Uniswap
def get_uniswap_price(base, quote):
    pair = base + '_' + quote
    response = requests.get(uniswap_api)
    for ticker in response.json()['tokens']:
        if ticker['pair'] == pair:
            return float(ticker['price'])


# Define a function to get the price of an asset pair from Paraswap
def get_paraswap_price(base, quote):
    params = {'from': base, 'to': quote, 'amount': '1'}
    response = requests.get(paraswap_api, params=params)
    return float(response.json()['price'])


# Define a function to find arbitrage opportunities
def find_arbitrage():
    for pair in asset_pairs:
        base, quote = pair
        oneinch_price = get_1inch_price(base, quote)
        uniswap_price = get_uniswap_price(base, quote)
        paraswap_price = get_paraswap_price(base, quote)
        if uniswap_price > oneinch_price * paraswap_price:
            print(f"Buy {base} on 1inch, sell on Paraswap and sell on Uniswap for a profit")
        elif uniswap_price * paraswap_price > oneinch_price:
            print(f"Buy {base} on Uniswap, sell on Paraswap and sell on 1inch for a profit")
        else:
            print(f"No arbitrage opportunity found for {base}/{quote}")


# Run the function to find arbitrage opportunities
find_arbitrage()
