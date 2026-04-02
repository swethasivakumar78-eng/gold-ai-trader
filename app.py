from flask import Flask, render_template, jsonify, request, send_file
import yfinance as yf
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------- GLOBAL PORTFOLIO ----------------
portfolio = {
    "balance": 0,
    "gold": 0,
    "initial": 0
}

# ---------------- LIVE GOLD PRICE ----------------
def get_gold_price_inr():
    try:
        import yfinance as yf

        if data.empty:
            return 7200

        usd_price = data["Close"].iloc[-1]

        usd_inr = yf.Ticker("USDINR=X").history(period="1d")["Close"].iloc[-1]

        price_inr = (usd_price * usd_inr) / 31.1035

        return round(price_inr, 2)

    except Exception as e:
        print("Price fetch error:", e)
        return 7200  # fallback

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- START ----------------
@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    amount = float(data.get("investment", 0))

    global portfolio
    portfolio["balance"] = amount
    portfolio["gold"] = 0
    portfolio["initial"] = amount

    price = get_gold_price_inr()

    return jsonify({
        "price": price,
        "action": "HOLD",
        "reward": 0,
        "balance": amount,
        "gold": 0,
        "profit": 0,
        "explanation": "Trading started"
    })
# ---------------- STEP ----------------
@app.route("/step")
def step():
    global portfolio

    price = get_gold_price_inr()

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

    total = portfolio["balance"] + portfolio["gold"] * price
    profit = total - portfolio["initial"]

    return jsonify({
        "price": round(price, 2),
        "action": action,
        "reward": round(profit, 2),
        "balance": round(portfolio["balance"], 2),
        "gold": round(portfolio["gold"], 4),
        "profit": round(profit, 2),
        "explanation": f"{action} executed"
    })

# ---------------- DOWNLOAD REPORT ----------------
@app.route("/download")
def download():
    text = f"""
GOLD REPORT

Initial: ₹{portfolio['initial']}
Balance: ₹{portfolio['balance']}
Gold: {portfolio['gold']} g
"""

    with open("report.txt", "w") as f:
        f.write(text)

    return send_file("report.txt", as_attachment=True)