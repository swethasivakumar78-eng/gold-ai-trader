let chart;
let prices = [];
let autoTradeInterval; // Holds our loop timer

console.log("JS LOADED");

// ---------------- CHART ----------------
function initChart() {
    const ctx = document.getElementById("chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Gold Price (1g INR)",
                data: [],
                borderWidth: 2,
                borderColor: '#FFD700',
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                fill: true
            }]
        }
    });
}

function updateChart(price) {
    prices.push(price);
    chart.data.labels.push(prices.length);
    chart.data.datasets[0].data = prices;
    chart.update();
}

// ---------------- START ----------------
function startTrading() {
    const investmentInput = document.getElementById("investment").value;
    const investment = Number(investmentInput);

    if (!investmentInput || isNaN(investment) || investment <= 0) {
        document.getElementById("explanation").innerText = "⚠️ Please enter a valid investment amount.";
        return;
    }

    // Tell the user it's loading
    document.getElementById("explanation").innerText = "Loading live market data...";

    fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ investment: investment })
    })
    .then(async res => {
        const data = await res.json();
        // If the server rejected it (like our 400 error), force it to show the error
        if (!res.ok) {
            throw new Error(data.error || "Network error");
        }
        return data;
    })
    .then(data => {
        // Success! Clear the chart and start the loop
        prices = [];
        chart.data.labels = [];
        updateUI(data);

        clearInterval(autoTradeInterval); 
        autoTradeInterval = setInterval(runStep, 10000);
    })
    .catch(err => {
        console.error("ERROR:", err);
        // Display the error directly on the screen so you can read it!
        document.getElementById("explanation").innerText = "⚠️ Error: " + err.message;
    });
}
// ---------------- STEP ----------------
function runStep() {
    fetch("/step")
    .then(res => res.json())
    .then(data => {
        if (!data.error) updateUI(data);
    })
    .catch(err => console.error("STEP ERROR:", err));
}

// ---------------- UI ----------------
function updateUI(data) {
    document.getElementById("price").innerText = data.price || 0;
    document.getElementById("action").innerText = data.action || "HOLD";
    document.getElementById("reward").innerText = data.reward || 0;
    document.getElementById("balance").innerText = data.balance || 0;
    document.getElementById("gold").innerText = data.gold || 0;
    document.getElementById("profit").innerText = data.profit || 0;
    document.getElementById("explanation").innerText = data.explanation || "No explanation";

    updateChart(data.price || 0);
}

// ---------------- REPORT ----------------
function downloadReport() {
    // FIX: Properly fetching the text from the HTML elements
    const priceText = document.getElementById("price").innerText;
    const actionText = document.getElementById("action").innerText;
    const profitText = document.getElementById("profit").innerText;

    const content = `Gold AI Trader Report\n----------------\nCurrent Price: ₹${priceText}\nLast Action: ${actionText}\nNet Profit: ₹${profitText}`;

    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "trading_report.txt";
    
    // Required for Firefox / stricter browsers
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ---------------- INIT ----------------
window.onload = function () {
    initChart();
    document.getElementById("startBtn").addEventListener("click", startTrading);
    document.getElementById("stepBtn").addEventListener("click", runStep);
    document.getElementById("downloadBtn").addEventListener("click", downloadReport);
};