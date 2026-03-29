from flask import Flask, request, jsonify, render_template
import random
import requests
import os
import pandas as pd
from stable_baselines3 import PPO

app = Flask(__name__)

# ---------------- GLOBALS ----------------
balance = 10000
gold = 0
current_step = 0

# ---------------- LOAD MODEL ----------------
model = None
df = None

def load_model():
    global model, df

    if model is None or df is None:
        try:
            print("Loading model...")
            model = PPO.load("gold_trading_model.zip")

            print("Loading dataset...")
            df = pd.read_csv("gold_and_macro_data.csv")

            print("Model loaded successfully")

        except Exception as e:
            print("MODEL LOAD ERROR:", e)
            model = None
            df = None


# ---------------- LIVE GOLD PRICE ----------------
ddef get_live_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        res = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        data = res.json()

        usd_price = data.get("price", 0)

        if usd_price == 0:
            raise Exception("Invalid API response")

        return round(usd_price * 83, 2)

    except Exception as e:
        print("API ERROR:", e)
        return 7200   # stable fallback (not random)

# ---------------- AI MODEL ACTION ----------------
def get_action():
    global current_step

    try:
        load_model()   # 🔥 IMPORTANT

        if model is None or df is None:
            return random.choice(["BUY", "SELL", "HOLD"])

        if current_step >= len(df):
            current_step = 0

        state = df.iloc[current_step].values

        action, _ = model.predict(state)

        current_step += 1

        if action == 0:
            return "HOLD"
        elif action == 1:
            return "BUY"
        elif action == 2:
            return "SELL"

        return "HOLD"

    except Exception as e:
        print("ACTION ERROR:", e)
        return "HOLD"


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global balance, gold

    data = request.get_json()

    if not data or "investment" not in data:
        return jsonify({
            "price": 7200,
            "action": "HOLD",
            "reward": 0,
            "balance": balance,
            "gold": gold,
            "profit": 0,
            "explanation": "Investment missing"
        })

    try:
        investment = float(data.get("investment", 0))
    except:
        investment = 0

    if investment <= 0:
        return jsonify({
            "price": 7200,
            "action": "HOLD",
            "reward": 0,
            "balance": balance,
            "gold": gold,
            "profit": 0,
            "explanation": "Invalid investment"
        })

    price = get_live_gold_price()
    action = get_action()

    reward = random.uniform(-5, 5)

    if action == "BUY":
        gold += investment / price
        balance -= investment
    elif action == "SELL" and gold > 0:
        balance += gold * price
        gold = 0

    profit = balance + gold * price - 10000

    return jsonify({
        "price": price,
        "action": action,
        "reward": round(reward, 2),
        "balance": round(balance, 2),
        "gold": round(gold, 4),
        "profit": round(profit, 2),
        "explanation": f"AI decided to {action}"
    })


@app.route("/step")
def step():
    global balance, gold

    price = get_live_gold_price()
    action = get_action()

    reward = random.uniform(-5, 5)

    profit = balance + gold * price - 10000

    return jsonify({
        "price": price,
        "action": action,
        "reward": round(reward, 2),
        "balance": round(balance, 2),
        "gold": round(gold, 4),
        "profit": round(profit, 2),
        "explanation": f"Market suggests {action}"
    })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))