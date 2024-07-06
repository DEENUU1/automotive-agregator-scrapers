function createScraperChart(scraperData) {
    var ctx = document.getElementById('lineChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: scraperData.map(item => item.run_date),
            datasets: [{
                label: 'Total Time',
                data: scraperData.map(item => item.total_time),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Run Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Total Time'
                    }
                }
            }
        }
    });
}

function createParserChart(parserData) {
    var ctx = document.getElementById('lineChart2').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: parserData.map(item => item.run_date),
            datasets: [{
                label: 'Saved Elements',
                data: parserData.map(item => item.saved_elements),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Run Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Saved elements'
                    }
                }
            }
        }
    });
}