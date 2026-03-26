let chart;

function start() {
    let amount = document.getElementById("amount").value;

    fetch('/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: amount})
    });
}

function step() {
    fetch('/step')
    .then(res => res.json())
    .then(data => {

        document.getElementById("price").innerText = data.price;
        document.getElementById("action").innerText = data.action;
        document.getElementById("reward").innerText = data.reward;

        document.getElementById("balance").innerText = data.balance;
        document.getElementById("gold").innerText = data.gold;
        document.getElementById("profit").innerText = data.profit;

        document.getElementById("explanation").innerText = data.explanation;

        updateChart(data.history);
    });
}

function updateChart(history) {
    if (!chart) {
        chart = new Chart(document.getElementById("chart"), {
            type: 'line',
            data: {
                labels: history,
                datasets: [{
                    label: "Gold Price",
                    data: history
                }]
            }
        });
    } else {
        chart.data.labels = history;
        chart.data.datasets[0].data = history;
        chart.update();
    }
}

function download() {
    window.location.href = "/report";
}