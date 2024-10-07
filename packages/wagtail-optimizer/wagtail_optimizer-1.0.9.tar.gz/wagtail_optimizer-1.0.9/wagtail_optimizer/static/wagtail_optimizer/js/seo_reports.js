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

let globalComputedStyles = null;

function getCssColorVariable(name) {
    if (!globalComputedStyles) {
        globalComputedStyles = getComputedStyle(document.documentElement);
    }
    return globalComputedStyles.getPropertyValue(name);
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
    const analysis = parseJSONScript('latest-analysis-seo-score');

    const colorGreen = getCssColorVariable('--w-color-secondary');
    const colorDanger = getCssColorVariable('--w-color-critical-100');
    const colorWarning = getCssColorVariable('--w-color-warning-100');

    const configScore = {
        "type": "line",
        "data": {
            "labels": scores.map(parseScoreDate),
            "datasets": [{
                "label": "SEO Score",
                "data": scores.map(score => score.seo_score),
                "borderColor": colorGreen,
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
    configErrors.data.datasets[0].borderColor = colorDanger;
    configErrors.data.datasets.push({
        "label": "Warnings",
        "data": errors.map(error => error.warning_count),
        "borderColor": colorWarning,
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

    const ctxScore = document.getElementById('seo-score-chart').getContext('2d');
    new Chart(ctxScore, configScore);

    const ctxErrors = document.getElementById('seo-errors-chart').getContext('2d');
    new Chart(ctxErrors, configErrors);

    if (analysis) {
        const configCurrentScore = {
            "type": "doughnut",
            "data": {
                "labels": [
                    analysis.label,
                ],
                "datasets": [{
                    "data": [analysis.value, 100 - analysis.value],
                    "backgroundColor": [colorGreen, colorDanger],
                }]
            },
            "options": {
                "plugins": {
                    "legend": {
                        "display": false,
                    },
                    "title": {
                        "display": true,
                        "text": analysis.title,
                        "color": getCssColorVariable('--w-color-text'),
                        "font": {
                            "size": 16,
                            "weight": "bold",
                        },
                    },
                },
            },
        }

        const ctxCurrentScore = document.getElementById('seo-current-score-chart').getContext('2d');
        new Chart(ctxCurrentScore, configCurrentScore);
    };
});