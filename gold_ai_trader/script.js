let chart;
let stepCount = 0;
let autoInterval = null;

function initChart() {
    const ctx = document.getElementById('chart').getContext('2d');

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Gold Price',
                    data: [],
                    borderColor: 'gold',
                    tension: 0.3
                },
                {
                    label: 'Profit',
                    data: [],
                    borderColor: 'lime',
                    tension: 0.3
                },
                {
                    label: 'Buy',
                    data: [],
                    pointBackgroundColor: 'green',
                    showLine: false
                },
                {
                    label: 'Sell',
                    data: [],
                    pointBackgroundColor: 'red',
                    showLine: false
                }
            ]
        }
    });
}

async function startTrading() {
    const investment = document.getElementById("investment").value;

    if (!investment) {
        alert("Enter investment amount!");
        return;
    }

    try {
        const res = await fetch("/start", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ investment: investment })
        });

        const data = await res.json();
        console.log("START DATA:", data);

        updateUI(data);

    } catch (err) {
        console.error("Start Error:", err);
        alert("Backend error!");
    }
}

async function runStep() {
    try {
        const res = await fetch("/step");
        const data = await res.json();

        console.log("STEP DATA:", data);

        updateUI(data);

    } catch (err) {
        console.error("Step Error:", err);
    }
}

// 🚀 AUTO TRADING LOOP
function startAutoTrading() {
    if (autoInterval) return;

    autoInterval = setInterval(() => {
        runStep();
    }, 2000); // every 2 seconds
}

function stopAutoTrading() {
    clearInterval(autoInterval);
    autoInterval = null;
}

// 📊 UPDATE UI + GRAPH
function updateUI(data) {
    document.getElementById("price").innerText = data.price;
    document.getElementById("action").innerText = data.action;
    document.getElementById("reward").innerText = data.reward;

    document.getElementById("balance").innerText = data.balance;
    document.getElementById("gold").innerText = data.gold;
    document.getElementById("profit").innerText = data.profit;

    document.getElementById("explanation").innerText = data.explanation;

    // GRAPH UPDATE
    stepCount++;

    chart.data.labels.push(stepCount);
    chart.data.datasets[0].data.push(data.price);
    chart.data.datasets[1].data.push(data.profit);

    // BUY/SELL MARKERS
    if (data.action === "BUY") {
        chart.data.datasets[2].data.push(data.price);
        chart.data.datasets[3].data.push(null);
    } else if (data.action === "SELL") {
        chart.data.datasets[3].data.push(data.price);
        chart.data.datasets[2].data.push(null);
    } else {
        chart.data.datasets[2].data.push(null);
        chart.data.datasets[3].data.push(null);
    }

    chart.update();
}

// DOWNLOAD
function downloadReport() {
    window.location.href = "/download";
}

// INIT
window.onload = initChart;