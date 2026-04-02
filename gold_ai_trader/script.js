let chart;
let prices = [];
let actions = [];
let interval;

console.log("JS LOADED SUCCESSFULLY");

// ---------------- CHART ----------------
function initChart() {
    const canvas = document.getElementById("chart");

    if (!canvas) {
        console.error("Chart canvas not found ");
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
                borderWidth: 2,
                tension: 0.3,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}

// ---------------- UPDATE CHART ----------------
function updateChart(price, action) {
    if (!chart) return;

    prices.push(price);
    actions.push(action);

    chart.data.labels.push(prices.length);
    chart.data.datasets[0].data = prices;

    // BUY/SELL MARKERS
    let colors = actions.map(a => {
        if (a === "BUY") return "green";
        if (a === "SELL") return "red";
        return "blue";
    });

    chart.data.datasets[0].pointBackgroundColor = colors;

    chart.update();
}

// ---------------- START ----------------
function startTrading() {
    console.log("Start button clicked");

    const investment = document.getElementById("investment").value;

    if (!investment || investment <= 0) {
        alert("Enter valid investment");
        return;
    }

    fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ investment: investment })
    })
    .then(res => {
        console.log("Start response status:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("START DATA:", data);

        // UI UPDATE
        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        // GRAPH UPDATE 
        updateChart(data.price, data.action);
    })
    .catch(err => {
        console.error("START ERROR:", err);
    });
}

// ---------------- STEP ----------------
function runStep() {
    console.log("Run Step clicked");

    fetch("/step")
    .then(res => res.json())
    .then(data => {
        console.log("STEP DATA:", data);

        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        // GRAPH UPDATE 
        updateChart(data.price, data.action);
    })
    .catch(err => console.error("STEP ERROR:", err));
}

// ---------------- AUTO TRADING ----------------
function startAutoTrading() {
    console.log("Auto trading started");

    interval = setInterval(() => {
        runStep();
    }, 2000);
}

function stopAutoTrading() {
    console.log("Auto trading stopped ");
    clearInterval(interval);
}

// ---------------- DOWNLOAD ----------------
function downloadReport() {
    window.location.href = "/download";
}

// ---------------- INIT ----------------
window.onload = function () {
    console.log("Window loaded ");
    initChart();
};