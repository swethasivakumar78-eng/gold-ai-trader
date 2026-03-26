let prices = [];
let profits = [];

let chart;

function initChart() {
    const ctx = document.getElementById('chart').getContext('2d');

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Gold Price',
                    data: prices,
                    borderWidth: 2
                },
                {
                    label: 'Profit',
                    data: profits,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true
        }
    });
}

async function startTrading() {
    const investment = document.getElementById("investment").value;

    const res = await fetch("/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ investment: investment })
    });

    const data = await res.json();
    updateUI(data);
}

async function runStep() {
    const res = await fetch("/step");
    const data = await res.json();
    updateUI(data);
}

function downloadReport() {
    window.location.href = "/download";
}

function updateUI(data) {
    document.getElementById("price").innerText = data.price;
    document.getElementById("action").innerText = data.action;
    document.getElementById("reward").innerText = data.reward;

    document.getElementById("balance").innerText = data.balance;
    document.getElementById("gold").innerText = data.gold;
    document.getElementById("profit").innerText = data.profit;

    document.getElementById("explanation").innerText = data.explanation;

    // Update chart
    prices.push(data.price);
    profits.push(data.profit);

    chart.data.labels.push(prices.length);
    chart.update();
}

// Initialize chart on load
window.onload = initChart;