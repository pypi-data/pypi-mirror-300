function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class ProgressBar {
    constructor(progressUrl, options) {
        this.progressUrl = progressUrl;
        this.options = options;
        this.interval = options.interval || 250;
        this.onProgress = options.onProgress || function() {};
        this.onResult = options.onResult || function() {};
        this._interval = null;
        this.start();
    }

    async _fetchProgress() {
        const response = await fetch(this.progressUrl, {
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });
        const data = await response.json();
        
        this.onProgress(data);

        if (data.complete) {
            this.stop();
            this.onResult(data.result);
        }
    }

    async start() {
        this._interval = setInterval(
            this._fetchProgress.bind(this),
            this.interval,
        );
    }

    stop() {
        if (!this._interval) {
            return
        }
        clearInterval(this._interval);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.wagtail-optimizer-form');
    const loaderWrapper = document.querySelector('.wagtail-optimizer-loader-wrapper');
    const loader = document.querySelector('.wagtail-optimizer-loader__bar');
    const loaderText = document.querySelector('.wagtail-optimizer-loader__text');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Serialize the form data
        const formData = new FormData(form);
        
        // JSONify the form data
        const data = {};
        formData.forEach(function(value, key){
            data[key] = value;
        });

        // Send the form data to the server
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data),
        })
        
        const responseData = await response.json();
        if (responseData.form_html) {
            form.innerHTML = responseData.form_html;
            return;
        }

        form.remove();

        loaderWrapper.classList.remove('hidden');

        const progressBar = new ProgressBar(responseData.progress_url, {
            onProgress: function(data) {
                console.log(data);
                loader.style.width = data.progress.percent + '%';
                loaderText.textContent = data.progress.description;
            },
            onResult: function(result) {
                if (result.result_url) {
                    window.location.href = result.result_url;
                }
            },
        });
    })
})