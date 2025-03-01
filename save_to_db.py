import psycopg2
import requests

# The Graph API endpoint for Uniswap v3
url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

query = """
{
  pools(first: 5, orderBy: volumeUSD, orderDirection: desc) {
    id
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    feeTier
    liquidity
    volumeUSD
  }
}
"""

# Fetch data from The Graph API
response = requests.post(url, json={'query': query})
data = response.json()
pools = data.get("data", {}).get("pools", [])

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="uniswap_data",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert data into PostgreSQL
for pool in pools:
    cur.execute("""
        INSERT INTO pools (id, token0, token1, feeTier, liquidity, volumeUSD)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE 
        SET liquidity = EXCLUDED.liquidity, volumeUSD = EXCLUDED.volumeUSD;
    """, (
        pool["id"],
        pool["token0"]["symbol"],
        pool["token1"]["symbol"],
        pool["feeTier"],
        pool["liquidity"],
        pool["volumeUSD"]
    ))

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("Data successfully saved to PostgreSQL!")

