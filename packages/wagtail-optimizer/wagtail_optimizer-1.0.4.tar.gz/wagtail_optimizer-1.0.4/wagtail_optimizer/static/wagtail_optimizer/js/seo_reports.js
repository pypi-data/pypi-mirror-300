document.addEventListener('DOMContentLoaded', function() {
    const scoresElem = document.getElementById('reports-seo-scores');
    let scores = [];
    try {
        scores = JSON.parse(scoresElem.textContent);
    } catch (e) {
        scores = [];
    }

    function parseScoreDate(score) {
        const createdAt = new Date(score.created_at);
        return createdAt.toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'short',
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
        });
    }

    const config = {
        "type": "line",
        "data": {
            "labels": scores.map(parseScoreDate),
            "datasets": [{
                "label": "SEO Score",
                "data": scores.map(score => score.seo_score),
                "fill": false,
                "borderColor": "rgb(75, 192, 192)",
                "lineTension": 0.1
            }]
        },
        "options": {
            "layout": {
                "padding": 0,
            },
            "plugins": {
                "legend": {
                    "display": false
                }
            },
            "elements": {
                "point": {
                    "radius": 8,
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": true,
                    "suggestedMax": 100
                },
                "x": {
                    "display": false,
                },
            },
        },
    }

    const ctx = document.getElementById('seo-score-chart').getContext('2d');
    new Chart(ctx, config);
});