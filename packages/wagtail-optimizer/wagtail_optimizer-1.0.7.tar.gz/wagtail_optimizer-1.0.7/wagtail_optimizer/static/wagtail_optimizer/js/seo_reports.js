function parseJSONScript(id) {
    const elem = document.getElementById(id);
    if (!elem) {
        return [];
    }
    try {
        return JSON.parse(elem.textContent);
    } catch (e) {
        return [];
    }
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

document.addEventListener('DOMContentLoaded', function() {
    const scores =parseJSONScript('reports-seo-scores');
    const errors =parseJSONScript('reports-error-counts');
    const currentScore = parseJSONScript('latest-analysis-seo-score');

    const configScore = {
        "type": "line",
        "data": {
            "labels": scores.map(parseScoreDate),
            "datasets": [{
                "label": "SEO Score",
                "data": scores.map(score => score.seo_score),
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

    const configErrors = JSON.parse(JSON.stringify(configScore));
    configErrors.data.labels = errors.map(parseScoreDate);
    configErrors.data.datasets[0].label = "Errors";
    configErrors.data.datasets[0].data = errors.map(error => error.error_count);
    configErrors.data.datasets[0].borderColor = "rgb(255, 99, 132)";
    configErrors.data.datasets.push({
        "label": "Warnings",
        "data": errors.map(error => error.warning_count),
        "borderColor": "rgb(255, 205, 86)",
        "lineTension": 0.1
    });
    configErrors.data.datasets.push({
        "label": "Aggregate",
        "data": errors.map(error => error.error_count + error.warning_count),
        "fill": false,
        "borderColor": "rgb(92, 27, 153)",
        "lineTension": 0.1,
        "hidden": true,
    });

    delete configErrors.options.scales.y.suggestedMax;
    delete configErrors.options.plugins.legend.display;

    const configCurrentScore = {
        "type": "doughnut",
        "data": {
            "labels": [currentScore.label],
            "datasets": [{
                "data": [currentScore.value, 100 - currentScore.value],
                "backgroundColor": ["rgb(75, 192, 192)", "rgb(255, 99, 132)"],
            }]
        },
        "options": {
            "plugins": {
                "legend": {
                    "onClick": (e) => e.stopPropagation(),
                }
            },
        },
    }

    const ctxScore = document.getElementById('seo-score-chart').getContext('2d');
    new Chart(ctxScore, configScore);

    const ctxCurrentScore = document.getElementById('seo-current-score-chart').getContext('2d');
    new Chart(ctxCurrentScore, configCurrentScore);

    const ctxErrors = document.getElementById('seo-errors-chart').getContext('2d');
    new Chart(ctxErrors, configErrors);
});