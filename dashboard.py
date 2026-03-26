import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from stable_baselines3 import PPO
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(layout="wide")

# =========================
# TITLE
# =========================
st.markdown("""
<h1 style='text-align:center; color:#00c3ff;'>
Explainable Multi-Agent Deep Reinforcement Learning
</h1>
<h3 style='text-align:center; color:gray;'>
Dynamic Gold Portfolio Strategy with Real-Time Price Integration
</h3>
<hr>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = PPO.load("gold_trading_model")

# =========================
# LOAD DATA
# =========================
df = yf.download("GC=F", period="6mo")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.dropna()

# =========================
# FEATURES
# =========================
df["SMA"] = df["Close"].rolling(20).mean()
df["Volatility"] = df["Close"].rolling(10).std()

delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

rs = gain.rolling(14).mean() / loss.rolling(14).mean()
df["RSI"] = 100 - (100/(1+rs))

df = df.bfill()

features = df[["Close","SMA","Volatility","RSI"]]

def fix(x):
    return np.pad(np.nan_to_num(x),(0,11-len(x)))[:11]

latest = fix(features.iloc[-1].values.astype(np.float32))

# =========================
# MULTI-AGENT SYSTEM
# =========================
st.markdown("##  Multi-Agent System")

ppo_action,_ = model.predict(latest)
ppo_action = int(ppo_action)

risk_action = 2 if latest[2] > 50 else ppo_action
trend_action = 1 if latest[0] > latest[1] else 2

agent_map = {0:"HOLD",1:"BUY",2:"SELL"}

st.write("PPO Agent:", agent_map[ppo_action])
st.write("Risk Agent:", agent_map[risk_action])
st.write("Trend Agent:", agent_map[trend_action])

decision = max(set([ppo_action,risk_action,trend_action]), key=[ppo_action,risk_action,trend_action].count)

st.success(f"Final Decision: {agent_map[decision]}")

# =========================
# EXPLAINABLE AI
# =========================
st.markdown("## Explainable AI")

explanations = []

if latest[0] > latest[1]:
    explanations.append("Uptrend detected (Price > SMA)")
else:
    explanations.append("Downtrend detected (Price < SMA)")

if latest[3] > 70:
    explanations.append("RSI Overbought → Possible SELL")
elif latest[3] < 30:
    explanations.append("RSI Oversold → Possible BUY")

if latest[2] > 50:
    explanations.append("High volatility → Risky market")

for e in explanations:
    st.write("✔", e)

# =========================
# REAL-TIME DATA
# =========================
st.markdown("##  Real-Time Data")

usd_price = df["Close"].iloc[-1]
price_inr = usd_price * 83 / 31.1

st.metric("Gold Price (₹/gram)", f"{price_inr:.2f}")

# =========================
# SIMULATION
# =========================
st.markdown("##  Simulation + Portfolio")

investment = st.number_input("Enter Investment (₹)", value=100000)

if st.button(" Run Simulation"):

    portfolio = investment
    values = []

    for i in range(len(features)):
        state = fix(features.iloc[i].values.astype(np.float32))
        act,_ = model.predict(state)

        price = df["Close"].iloc[i]

        if act == 1:
            portfolio += price * 0.01
        elif act == 2:
            portfolio -= price * 0.01

        values.append(portfolio)

    st.success(f"Final Portfolio Value: ₹{portfolio:.2f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=values))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# GRAPHS
# =========================
st.markdown("##  Graphs")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df.index, y=df["Close"]))
st.plotly_chart(fig2, use_container_width=True)

# =========================
# REPORT
# =========================
st.markdown("##  Report")

def generate_pdf():

    plt.plot(df["Close"])
    plt.title("Gold Price Trend")
    plt.savefig("graph.png")
    plt.close()

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Gold AI Trading Report", styles["Title"]))
    content.append(Spacer(1,20))

    content.append(Paragraph(f"Decision: {agent_map[decision]}", styles["Normal"]))
    content.append(Paragraph(f"Gold Price: ₹{price_inr:.2f}", styles["Normal"]))

    content.append(Paragraph("Explanation:", styles["Heading2"]))
    for e in explanations:
        content.append(Paragraph(e, styles["Normal"]))

    content.append(Image("graph.png", width=400, height=200))

    doc.build(content)
    return "report.pdf"

if st.button(" Download Report"):
    pdf = generate_pdf()
    with open(pdf, "rb") as f:
        st.download_button("Download PDF", f)