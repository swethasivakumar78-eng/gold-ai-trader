let chart;
let prices = [];

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
        body: JSON.stringify({ investment: investment })
    })
    .then(res => {
        console.log("Status:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("START RESPONSE:", data);

        if (!data || !data.price) {
            alert("Invalid response from server");
            return;
        }

        updateUI(data);
    })
    .catch(err => {
        console.error("START ERROR:", err);
        alert("Backend not responding");
    });
}

// ---------------- STEP ----------------
function runStep() {
    console.log("Calling STEP API...");

    fetch(window.location.origin + "/step")
    .then(res => {
        console.log("STEP Status:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("STEP RESPONSE:", data);

        if (!data || !data.price) {
            console.error("Invalid step data");
            return;
        }

        updateUI(data);
    })
    .catch(err => console.error("STEP ERROR:", err));
}