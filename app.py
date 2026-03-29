from flask import Flask, request, jsonify, render_template
import random
import requests
import os

app = Flask(__name__)

balance = 10000
gold = 0
price_history = []


# LIVE GOLD PRICE
def get_live_gold_price():
    try:
        res = requests.get(
            "https://api.metals.live/v1/spot/gold",
            timeout=5
        )
        data = res.json()
        return round(data[0][1] * 83, 2)  # USD → INR
    except Exception as e:
        print("API ERROR:", e)
        return random.randint(7000, 7500)


# SIMPLE AI LOGIC
def get_action(price):
    price_history.append(price)

    if len(price_history) < 2:
        return "HOLD"

    if price > price_history[-2]:
        return "BUY"
    elif price < price_history[-2]:
        return "SELL"
    return "HOLD"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global balance, gold

    data = request.json
    investment = float(data["investment"])

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
        "explanation": f"AI decided to {action} based on trend"
    })


@app.route("/step")
def step():
    global balance, gold

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
        "explanation": f"Market trend suggests {action}"
    })


# IMPORTANT FOR RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))