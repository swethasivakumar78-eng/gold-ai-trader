import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

print("Loading dataset...")

df = pd.read_csv("processed_features.csv")

# keep only numeric columns
df = df.select_dtypes(include=[np.number])

print("Dataset columns used for model:")
print(df.columns)

print("Loading trained model...")
model = PPO.load("gold_trading_model")

prices = df.iloc[:,0].values

buy_points = []
sell_points = []

ai_portfolio = 100000
hold_portfolio = 100000

ai_values = []
hold_values = []

start_price = prices[0]

print("Running AI simulation...")

for i in range(len(df)):

    state = df.iloc[i].values.astype(np.float32)

    # remove NaN
    state = np.nan_to_num(state)

    action,_ = model.predict(state)

    price = prices[i]

    if action == 1:
        buy_points.append(i)
        ai_portfolio += price * 0.01

    elif action == 2:
        sell_points.append(i)
        ai_portfolio -= price * 0.01

    hold_portfolio = 100000 * (price / start_price)

    ai_values.append(ai_portfolio)
    hold_values.append(hold_portfolio)

print("Generating graphs...")

# Graph 1: Buy Sell Signals
plt.figure(figsize=(12,6))

plt.plot(prices,label="Gold Price")

plt.scatter(buy_points,prices[buy_points],marker="^",label="Buy")
plt.scatter(sell_points,prices[sell_points],marker="v",label="Sell")

plt.title("AI Trading Signals on Gold Price")
plt.xlabel("Time")
plt.ylabel("Gold Price")
plt.legend()

plt.show()


# Graph 2: Portfolio Growth
plt.figure(figsize=(10,5))

plt.plot(ai_values,label="AI Portfolio Value")

plt.title("Portfolio Value Over Time")
plt.xlabel("Time")
plt.ylabel("Portfolio Value")
plt.legend()

plt.show()


# Graph 3: AI vs Buy Hold
plt.figure(figsize=(10,5))

plt.plot(ai_values,label="AI Strategy")
plt.plot(hold_values,label="Buy & Hold")

plt.title("AI Strategy vs Buy and Hold")
plt.xlabel("Time")
plt.ylabel("Portfolio Value")
plt.legend()

plt.show()

print("Graphs generated successfully!")