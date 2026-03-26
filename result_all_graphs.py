import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
import shap

print("Loading dataset...")

df = pd.read_csv("processed_features.csv")

# keep numeric columns only
df = df.select_dtypes(include=[np.number])

prices = df.iloc[:,0].values

print("Loading trained model...")
model = PPO.load("gold_trading_model")

buy = []
sell = []

portfolio = 100000
portfolio_values = []

print("Running AI simulation...")

for i in range(len(df)):

    state = df.iloc[i].values.astype(np.float32)
    state = np.nan_to_num(state)

    action,_ = model.predict(state)

    price = prices[i]

    if action == 1:
        buy.append(i)
        portfolio += price * 0.01

    elif action == 2:
        sell.append(i)
        portfolio -= price * 0.01

    portfolio_values.append(portfolio)

print("Creating graphs...")

# -----------------------------
# Graph 1: Gold Price Trend
# -----------------------------

plt.figure(figsize=(10,5))
plt.plot(prices)

plt.title("Gold Price Trend")
plt.xlabel("Time")
plt.ylabel("Gold Price")

plt.show()


# -----------------------------
# Graph 2: Trading Decisions
# -----------------------------

plt.figure(figsize=(12,6))

plt.plot(prices,label="Gold Price")

plt.scatter(buy,prices[buy],marker="^",label="Buy Signal")
plt.scatter(sell,prices[sell],marker="v",label="Sell Signal")

plt.title("AI Trading Decisions")
plt.xlabel("Time")
plt.ylabel("Price")

plt.legend()

plt.show()


# -----------------------------
# Graph 3: Portfolio Value
# -----------------------------

plt.figure(figsize=(10,5))

plt.plot(portfolio_values,label="Portfolio Value")

plt.title("Portfolio Value Over Time")
plt.xlabel("Time")
plt.ylabel("Portfolio Value")

plt.legend()

plt.show()


# -----------------------------
# Graph 4: Feature Importance
# -----------------------------

print("Generating SHAP feature importance...")

X = df

explainer = shap.Explainer(lambda x: x.mean(axis=1), X)

shap_values = explainer(X)

shap.summary_plot(shap_values, X)

print("All graphs generated successfully!")