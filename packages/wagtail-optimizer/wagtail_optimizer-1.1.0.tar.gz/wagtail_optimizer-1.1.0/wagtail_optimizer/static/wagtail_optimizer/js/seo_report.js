document.addEventListener('DOMContentLoaded', function() {
    var wrappers = document.getElementsByClassName("seo-accordion-wrapper");

    for (let i = 0; i < wrappers.length; i++) {
        const wrapper = wrappers[i];
        const accordion = wrapper.querySelector('.seo-accordion');
        const panel = wrapper.querySelector('.seo-panel');

        accordion.addEventListener("click", function(event) {
            if (event.target.tagName === "A") {
                return;
            }

            this.classList.toggle("active");

            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }
});