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
                borderColor: "gold",
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

    if (!investment) {
        alert("Enter amount");
        return;
    }

    fetch("/start", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ investment: investment })
    })
    .then(res => res.json())
    .then(data => updateUI(data))
    .catch(err => console.error(err));
}

// ---------------- STEP ----------------
function runStep() {
    fetch("/step")
    .then(res => res.json())
    .then(data => updateUI(data))
    .catch(err => console.error(err));
}

// ---------------- UPDATE UI ----------------
function updateUI(data) {
    document.getElementById("price").innerText = data.price;
    document.getElementById("action").innerText = data.action;
    document.getElementById("reward").innerText = data.reward;

    document.getElementById("balance").innerText = data.balance;
    document.getElementById("gold").innerText = data.gold;
    document.getElementById("profit").innerText = data.profit;

    document.getElementById("explanation").innerText = data.explanation;

    updateChart(data.price);
}

// ---------------- DOWNLOAD ----------------
function downloadReport() {
    window.location.href = "/download";
}

// ---------------- INIT ----------------
window.onload = initChart;