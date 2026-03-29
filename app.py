from flask import Flask, render_template, jsonify, request, send_file
import yfinance as yf
import random

app = Flask(__name__)

# ---------------------------
# GLOBAL PORTFOLIO
# ---------------------------
portfolio = {
    "balance": 0,
    "gold": 0,
    "initial": 0
}

# ---------------------------
# LIVE GOLD PRICE FUNCTION
# ---------------------------
def get_gold_price_inr():
    try:
        gold = yf.Ticker("GC=F")  # Gold futures (USD)
        data = gold.history(period="1d")

        if len(data) == 0:
            return 7200

        usd_price = data['Close'].iloc[-1]

        usd_inr = yf.Ticker("USDINR=X").history(period="1d")['Close'].iloc[-1]

        price_inr = (usd_price * usd_inr) / 31.1035

        return round(price_inr, 2)

    except Exception as e:
        print("Price Fetch Error:", e)
        return 7200  # fallback

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------------------
# START TRADING
# ---------------------------
@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    amount = float(data.get("investment", 0))

    global portfolio
    portfolio = {
        "balance": amount,
        "gold": 0,
        "initial": amount
    }

    price = get_gold_price_inr()

    return jsonify({
        "price": price,
        "action": "HOLD",
        "reward": 0,
        "balance": portfolio["balance"],
        "gold": portfolio["gold"],
        "profit": 0,
        "explanation": "Trading started successfully"
    })

# ---------------------------
# STEP (AI DECISION)
# ---------------------------
@app.route("/step")
def step():
    global portfolio

    price = get_gold_price_inr()

    # SIMPLE LOGIC (NO RANDOM BUGS)
    if portfolio["balance"] > 0:
        action = "BUY"
        portfolio["gold"] = portfolio["balance"] / price
        portfolio["balance"] = 0

    elif portfolio["gold"] > 0:
        action = "SELL"
        portfolio["balance"] = portfolio["gold"] * price
        portfolio["gold"] = 0

    else:
        action = "HOLD"

    total = portfolio["balance"] + (portfolio["gold"] * price)
    profit = total - portfolio["initial"]

    return jsonify({
        "price": round(price, 2),
        "action": action,
        "reward": round(profit, 2),
        "balance": round(portfolio["balance"], 2),
        "gold": round(portfolio["gold"], 4),
        "profit": round(profit, 2),
        "explanation": f"{action} executed based on portfolio state"
    })
# ---------------------------
# DOWNLOAD REPORT 
# ---------------------------
@app.route("/download")
def download():
    text = f"""
GOLD TRADING REPORT

Initial Investment: ₹{portfolio['initial']}
Current Balance: ₹{portfolio['balance']}
Gold Holdings: {portfolio['gold']} g

Thank you for using Gold AI Trader!
"""

    with open("report.txt", "w") as f:
        f.write(text)

    return send_file("report.txt", as_attachment=True)
# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    print("Server starting...")
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)