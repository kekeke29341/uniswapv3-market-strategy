import requests

def fetch_uniswap_data():
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    query = """
    {
      pools(first: 5, orderBy: volumeUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
        feeTier
        liquidity
        volumeUSD
      }
    }
    """
    response = requests.post(url, json={'query': query})
    return response.json()

print(fetch_uniswap_data())

