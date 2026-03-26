from flask import Flask, render_template, jsonify, request, send_file
import yfinance as yf
import numpy as np
from stable_baselines3 import PPO
import os
app = Flask(__name__)

# LOAD MODEL (safe)
try:
    model = PPO.load("gold_trading_model.zip")
    print(" Model Loaded")
except Exception as e:
    print(" Model Error:", e)
    model = None

portfolio = {"balance": 0, "gold": 0, "initial": 0}
previous_price = None
history = []

#  FAST GOLD PRICE (with fallback)
def get_gold_price_inr():
    try:
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")

        if len(data) == 0:
            return 7200

        usd_price = data['Close'].iloc[-1]
        usd_inr = yf.Ticker("USDINR=X").history(period="1d")['Close'].iloc[-1]

        return float((usd_price * usd_inr) / 31.1035)
    except:
        return 7200

# Explain AI
def explain(action, price, prev):
    if action == 1:
        return f"BUY → Uptrend ({prev:.2f} → {price:.2f})"
    elif action == 2:
        return f"SELL → Downtrend ({prev:.2f} → {price:.2f})"
    return "HOLD → Market uncertain"

# Trade logic
def trade(action, price):
    if action == 1 and portfolio["balance"] > 0:
        portfolio["gold"] = portfolio["balance"] / price
        portfolio["balance"] = 0

    elif action == 2 and portfolio["gold"] > 0:
        portfolio["balance"] = portfolio["gold"] * price
        portfolio["gold"] = 0

    total = portfolio["balance"] + portfolio["gold"] * price
    profit = total - portfolio["initial"]

    return total, profit

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    amount = float(request.json["amount"])

    portfolio["balance"] = amount
    portfolio["gold"] = 0
    portfolio["initial"] = amount

    return {"status": "started"}

@app.route("/step")
def step():
    global previous_price

    price = get_gold_price_inr()

    if previous_price is None:
        previous_price = price

    obs = np.array([price] * 11)

    # AI prediction
    if model:
        action, _ = model.predict(obs)
        action = int(action)
    else:
        action = np.random.choice([0,1,2])

    total, profit = trade(action, price)

    reward = total - portfolio["initial"]
    explanation = explain(action, price, previous_price)

    previous_price = price
    history.append(price)

    return jsonify({
        "price": round(price, 2),
        "action": ["HOLD", "BUY", "SELL"][action],
        "balance": round(portfolio["balance"], 2),
        "gold": round(portfolio["gold"], 4),
        "profit": round(profit, 2),
        "reward": round(reward, 2),
        "explanation": explanation,
        "history": history
    })

@app.route("/report")
def report():
    total = portfolio["balance"] + portfolio["gold"] * previous_price
    profit = total - portfolio["initial"]

    text = f"""
GOLD TRADING AI REPORT

Initial Investment: ₹{portfolio['initial']}
Final Value: ₹{round(total,2)}
Profit: ₹{round(profit,2)}

AI Strategy:
- Buy during upward trends
- Sell during downward trends
- Hold during uncertainty
"""

    with open("report.txt", "w") as f:
        f.write(text)

    return send_file("report.txt", as_attachment=True)

#  FAST RUN (no double reload)
if __name__ == "__main__":
    print("Server starting...")
   

if __name__ == "__main__":
    print(" Server starting...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)