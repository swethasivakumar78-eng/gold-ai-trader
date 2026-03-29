let chart;
let prices = [];

console.log("JS LOADED");

// ---------------- CHART ----------------
function initChart() {
    const ctx = document.getElementById("chart").getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Gold Price",
                data: [],
                borderWidth: 2
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
    const investment = document.getElementById("investment").value;

    if (!investment || investment <= 0) {
        alert("Enter valid investment");
        return;
    }

    console.log("Calling START API...");

    fetch(window.location.origin + "/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            investment: Number(investment)
        })
    })
    .then(res => {
        console.log("Status:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("START RESPONSE:", data);
        updateUI(data);
    })
    .catch(err => console.error("ERROR:", err));
}

// ---------------- STEP ----------------
function runStep() {
    console.log("Calling STEP API...");

    fetch(window.location.origin + "/step")
    .then(res => res.json())
    .then(data => {
        console.log("STEP RESPONSE:", data);
        updateUI(data);
    })
    .catch(err => console.error("STEP ERROR:", err));
}

// ---------------- UI ----------------
function updateUI(data) {
    console.log("UI DATA:", data);

    document.getElementById("price").innerText = data.price || 0;
    document.getElementById("action").innerText = data.action || "HOLD";
    document.getElementById("reward").innerText = data.reward || 0;

    document.getElementById("balance").innerText = data.balance || 0;
    document.getElementById("gold").innerText = data.gold || 0;
    document.getElementById("profit").innerText = data.profit || 0;

    document.getElementById("explanation").innerText =
        data.explanation || "No explanation";

    updateChart(data.price || 0);
}

// ---------------- REPORT ----------------
function downloadReport() {
    const content = `
Gold AI Report
----------------
Price: ${price.innerText}
Action: ${action.innerText}
Profit: ${profit.innerText}
    `;

    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "report.txt";
    link.click();
}

// ---------------- INIT ----------------
window.onload = function () {
    console.log("Page Loaded");

    initChart();

    document.getElementById("startBtn").addEventListener("click", startTrading);
    document.getElementById("stepBtn").addEventListener("click", runStep);
    document.getElementById("downloadBtn").addEventListener("click", downloadReport);
};

// AUTO UPDATE
setInterval(runStep, 5000);