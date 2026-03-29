from flask import Flask, request, jsonify, render_template
import random
import requests
import os

app = Flask(__name__)

# ---------------- GLOBALS ----------------
balance = 10000
gold = 0

# ---------------- LIVE GOLD PRICE ----------------
def get_live_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        res = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        data = res.json()

        usd_price = data.get("price", 0)

        if usd_price == 0:
            raise Exception("Invalid API response")

        # Convert USD → INR
        return round(usd_price * 83, 2)

    except Exception as e:
        print("API ERROR:", e)
        return 14000   # fallback based on real Indian price

# ---------------- SMART TRADING LOGIC ----------------
def get_action(price):
    if price > 14500:
        return random.choice(["SELL", "HOLD"])
    elif price < 13500:
        return random.choice(["BUY", "HOLD"])
    else:
        return "HOLD"

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global balance, gold

    try:
        data = request.get_json()
        investment = float(data.get("investment", 0))

        if investment <= 0:
            raise Exception("Invalid investment")

        price = get_live_gold_price()
        action = get_action(price)

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
            "explanation": f"AI decided to {action} based on price level"
        })

    except Exception as e:
        print("START ERROR:", e)

        return jsonify({
            "price": 14000,
            "action": "HOLD",
            "reward": 0,
            "balance": balance,
            "gold": gold,
            "profit": 0,
            "explanation": "Fallback response"
        })

@app.route("/step")
def step():
    global balance, gold

    try:
        price = get_live_gold_price()
        action = get_action(price)

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

    except Exception as e:
        print("STEP ERROR:", e)

        return jsonify({
            "price": 14000,
            "action": "HOLD",
            "reward": 0,
            "balance": balance,
            "gold": gold,
            "profit": 0,
            "explanation": "Fallback step response"
        })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))