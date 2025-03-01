import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Uniswap v3 historical data (replace with actual API calls)
df = pd.read_csv("uniswap_v3_prices.csv")

# Define liquidity range
lower_bound = df['price'].mean() * 0.99
upper_bound = df['price'].mean() * 1.01

df['fees_earned'] = np.where(
    (df['price'] >= lower_bound) & (df['price'] <= upper_bound),
    df['volume'] * 0.003, # 0.3% fees
    0
)

plt.plot(df['time'], df['fees_earned'].cumsum(), label="Total Fees Earned")
plt.legend()
plt.show()
