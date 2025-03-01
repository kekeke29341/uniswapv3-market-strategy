import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load Uniswap v3 historical data (replace with actual API calls)
df = pd.read_csv("uniswap_v3_prices.csv")

def calculate_volatility(prices, window=20):
    return prices.pct_change().rolling(window).std()

def calculate_impermanent_loss(price_start, price_end):
    ratio = price_end / price_start
    return 2 * np.sqrt(ratio) / (1 + ratio) - 1

# Define dynamic liquidity range based on volatility
df['volatility'] = calculate_volatility(df['price'])
df['lower_bound'] = df['price'] * (1 - df['volatility'])
df['upper_bound'] = df['price'] * (1 + df['volatility'])

# Calculate fees earned
fee_rate = 0.003
df['fees_earned'] = np.where(
    (df['price'] >= df['lower_bound']) & (df['price'] <= df['upper_bound']),
    df['volume'] * fee_rate,
    0
)

# Calculate impermanent loss
initial_price = df['price'].iloc[0]
df['impermanent_loss'] = calculate_impermanent_loss(initial_price, df['price'])

# Plot results
plt.figure(figsize=(12,6))
plt.plot(df['time'], df['fees_earned'].cumsum(), label="Total Fees Earned")
plt.plot(df['time'], df['impermanent_loss'] * 100, label="Impermanent Loss (%)", linestyle='dashed')
plt.legend()
plt.show()
