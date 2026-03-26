import pandas as pd
from stable_baselines3 import PPO
from trading_env import GoldTradingEnv

print("Loading model...")

model = PPO.load("gold_trading_model")

print("Loading dataset...")

df = pd.read_csv("processed_features.csv")

if "Date" in df.columns:
    df = df.drop(columns=["Date"])

env = GoldTradingEnv(df)

state, _ = env.reset()

total_reward = 0

for step in range(len(df) - 1):

    action, _ = model.predict(state)

    state, reward, terminated, truncated, info = env.step(action)

    total_reward += reward

    if terminated:
        break

print("Total trading reward:", total_reward)