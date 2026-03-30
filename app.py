from flask import Flask, request, jsonify, render_template
import random
import requests
import os

app = Flask(__name__)

# ---------------- GLOBALS ----------------
balance = 10000.0
gold = 0.0

# ---------------- LIVE GOLD PRICE (INDIA) ----------------
def get_live_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"
        # Increased timeout to 15s to survive Render's slow "cold starts"
        res = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        data = res.json()

        usd_price_per_ounce = data.get("price", 0)

        if usd_price_per_ounce == 0:
            raise Exception("Invalid API response")

        # Convert USD to INR (Approx ₹83.5 per $1)
        # 1 Troy Ounce = 31.1035 grams
        inr_per_gram = (usd_price_per_ounce / 31.1035) * 83.5
        
        return round(inr_per_gram, 2)

    except Exception as e:
        print("API ERROR:", e)
        # Fallback to roughly ₹7500 per gram if the API is unreachable
        return 7500.00   

# ---------------- SMART TRADING LOGIC ----------------
def get_action(price):
    # Updated thresholds for 1 gram of gold in INR
    if price > 8000:
        return random.choice(["SELL", "HOLD"])
    elif price < 7000:
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
        # force=True makes Flask try to read the JSON even if headers are slightly off
        data = request.get_json(force=True, silent=True) or {}
        print("RECEIVED DATA:", data)  # This will log in Render so we can debug!

        investment = float(data.get("investment", 0))

        # Break the errors apart so you know exactly which one is triggering
        if investment <= 0:
            return jsonify({"error": "Enter an amount greater than 0"}), 400
            
        if investment > balance:
            return jsonify({"error": f"Insufficient funds! Your balance is only ₹{balance}"}), 400

        price = get_live_gold_price()
        action = get_action(price)
        reward = random.uniform(-5, 5)

        if action == "BUY":
            gold += investment / price
            balance -= investment
        elif action == "SELL" and gold > 0:
            balance += gold * price
            gold = 0

        profit = balance + (gold * price) - 10000

        return jsonify({
            "price": price,
            "action": action,
            "reward": round(reward, 2),
            "balance": round(balance, 2),
            "gold": round(gold, 4),
            "profit": round(profit, 2),
            "explanation": f"AI decided to {action} based on market price"
        })

    except Exception as e:
        print("START ERROR:", e)
        return jsonify({"error": "Failed to calculate start. Try again."}), 500

@app.route("/step")
def step():
    global balance, gold
    try:
        price = get_live_gold_price()
        action = get_action(price)
        reward = random.uniform(-5, 5)
        profit = balance + (gold * price) - 10000

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
        return jsonify({"error": "Server network error"}), 500

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))