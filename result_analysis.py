import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

print("Loading data...")

# =========================
# LOAD DATA
# =========================
df = yf.download("GC=F", period="6mo")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.dropna()

# =========================
# FEATURES
# =========================
df["SMA"] = df["Close"].rolling(20).mean()
df["Volatility"] = df["Close"].rolling(10).std()

delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

rs = gain.rolling(14).mean() / loss.rolling(14).mean()
df["RSI"] = 100 - (100/(1+rs))

df = df.bfill()

features = df[["Close","SMA","Volatility","RSI"]]

def fix(x):
    return np.pad(np.nan_to_num(x),(0,11-len(x)))[:11]

# =========================
# LOAD MODEL
# =========================
model = PPO.load("gold_trading_model")

# =========================
# SIMULATION
# =========================
print("Running simulation...")

investment = 100000
portfolio = investment

decisions = []
portfolio_values = []

for i in range(len(features)):

    state = fix(features.iloc[i].values.astype(np.float32))
    action,_ = model.predict(state)

    price = df["Close"].iloc[i]

    if action == 1:
        portfolio += price * 0.01
        decisions.append("BUY")
    elif action == 2:
        portfolio -= price * 0.01
        decisions.append("SELL")
    else:
        decisions.append("HOLD")

    portfolio_values.append(portfolio)

df["Decision"] = decisions
df["Portfolio"] = portfolio_values

# =========================
# SAVE TABLE
# =========================
df.to_csv("result_table.csv")
print("Saved result_table.csv")

# =========================
# GRAPH 1: GOLD PRICE
# =========================
plt.figure()
plt.plot(df.index, df["Close"])
plt.title("Gold Price Trend")
plt.savefig("gold_price.png")
plt.close()

# =========================
# GRAPH 2: PORTFOLIO
# =========================
plt.figure()
plt.plot(df.index, df["Portfolio"])
plt.title("Portfolio Value Over Time")
plt.savefig("portfolio.png")
plt.close()

print("Graphs saved!")

# =========================
# SUMMARY
# =========================
final_value = portfolio_values[-1]
profit = final_value - investment

print("Final Portfolio:", final_value)
print("Profit:", profit)