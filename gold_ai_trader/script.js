let chart;
let prices = [];

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

// START BUTTON FUNCTION
function startTrading() {
    const investment = document.getElementById("investment").value;

    console.log("Sending request...");

    fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            investment: investment
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response:", data);

        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        updateChart(data.price);
    });
}

//  STEP BUTTON
function runStep() {
    fetch("/step")
    .then(res => res.json())
    .then(data => {
        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        updateChart(data.price);
    });
}

// INIT CHART ON LOAD
window.onload = initChart;