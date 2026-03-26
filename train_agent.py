import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from trading_env import GoldTradingEnv

print("Starting script...")

# Load dataset
df = pd.read_csv("processed_features.csv")

print("Dataset loaded")

# Remove Date column if present
if "Date" in df.columns:
    df = df.drop(columns=["Date"])

print("Dataset shape:", df.shape)

# Create environment
def make_env():
    return GoldTradingEnv(df)

env = DummyVecEnv([make_env])

print("Environment created")

# Create PPO model
model = PPO("MlpPolicy", env, verbose=1)

print("Model created")
print("Starting training...")

model.learn(total_timesteps=20000)

print("Training finished")

model.save("gold_trading_model")

print("Model saved successfully!")