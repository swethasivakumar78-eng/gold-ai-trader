import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

print("Loading dataset...")

df = pd.read_csv("processed_features.csv")
df = df.select_dtypes(include=[np.number])

prices = df.iloc[:,0].values

print("Loading trained model...")
model = PPO.load("gold_trading_model")

portfolio = 100000
rewards = []

print("Simulating rewards...")

for i in range(len(df)):

    state = df.iloc[i].values.astype(np.float32)
    state = np.nan_to_num(state)

    action,_ = model.predict(state)

    price = prices[i]

    reward = 0

    if action == 1:
        reward = price * 0.01
        portfolio += reward

    elif action == 2:
        reward = -price * 0.01
        portfolio += reward

    rewards.append(reward)

# cumulative reward
cumulative_reward = np.cumsum(rewards)

plt.figure(figsize=(10,5))

plt.plot(cumulative_reward,label="Cumulative Reward")

plt.title("Reward Curve of RL Trading Agent")
plt.xlabel("Time Step")
plt.ylabel("Cumulative Reward")

plt.legend()

plt.show()

print("Reward curve generated successfully!")