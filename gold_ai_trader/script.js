let chart;
let prices = [];

console.log("JS LOADED SUCCESSFULLY");

// ---------------- CHART ----------------
function initChart() {
    const canvas = document.getElementById("chart");

    if (!canvas) {
        console.error("Chart canvas not found ❌");
        return;
    }

    const ctx = canvas.getContext("2d");

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
    if (!chart) return;

    prices.push(price);
    chart.data.labels.push(prices.length);
    chart.data.datasets[0].data = prices;
    chart.update();
}

// ---------------- START ----------------
function startTrading() {
    console.log("Start button clicked");

    const investment = document.getElementById("investment").value;

    if (!investment || investment <= 0) {
        alert("Enter valid investment amount");
        return;
    }

    console.log("Sending request...", investment);

    fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            investment: investment
        })
    })
    .then(res => {
        console.log("Response status:", res.status);
        return res.json();
    })
    .then(data => {   // CORRECT

        console.log("API RESPONSE:", data);

        if (!data.action) {
            console.error("Invalid API response", data);
            return;
        }

        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        updateChart(data.price);
    })
    .catch(err => {
        console.error("FETCH ERROR :", err);
    });
}

// ---------------- STEP ----------------
function runStep() {
    console.log("Run Step clicked");

    fetch("/step")
    .then(res => res.json())
    .then(data => {
        console.log("STEP RESPONSE:", data);

        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        updateChart(data.price);
    })
    .catch(err => console.error("STEP ERROR:", err));
}

// ---------------- INIT ----------------
window.onload = function () {
    console.log("Window loaded");
    initChart();
};