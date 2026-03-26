import pandas as pd
import numpy as np
from ta.momentum import rsi
from ta.trend import SMAIndicator
from ta.volatility import BollingerBands
from ta.others import daily_return

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(
    "gold_and_macro_data.csv",
    parse_dates=["Date"],
    index_col="Date"
)

print("Original Columns:", df.columns)


# -----------------------------
# Data Cleaning
# -----------------------------

# Fill missing macroeconomic values
df.ffill(inplace=True)

# Drop remaining NaN
df.dropna(inplace=True)


# -----------------------------
# Feature Engineering
# -----------------------------

# RSI
df["RSI"] = rsi(close=df["Close"], window=14)

# Moving averages
df["SMA_50"] = SMAIndicator(
    close=df["Close"],
    window=50
).sma_indicator()

df["SMA_200"] = SMAIndicator(
    close=df["Close"],
    window=200
).sma_indicator()

# Bollinger Bands
bb = BollingerBands(close=df["Close"], window=20)

df["BB_high"] = bb.bollinger_hband()
df["BB_low"] = bb.bollinger_lband()

# Daily Return
df["Daily_Return"] = daily_return(close=df["Close"])

# Volatility
df["Volatility"] = df["Close"].pct_change().rolling(window=14).std()


# -----------------------------
# Select useful columns
# -----------------------------

df = df[[
    "Close",
    "Volume",
    "CPIAUCSL",
    "DFF",
    "RSI",
    "SMA_50",
    "SMA_200",
    "BB_high",
    "BB_low",
    "Daily_Return",
    "Volatility"
]]


# -----------------------------
# Final Cleaning
# -----------------------------

df.dropna(inplace=True)


# -----------------------------
# Save processed dataset
# -----------------------------

df.to_csv("processed_features.csv")

print("\nPreprocessing complete")
print("Final dataset shape:", df.shape)
print(df.head())