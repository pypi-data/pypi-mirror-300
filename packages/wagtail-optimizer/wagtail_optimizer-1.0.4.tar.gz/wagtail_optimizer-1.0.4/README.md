wagtail_optimizer
================

A SEO tool for your wagtail pages.

Quick start
-----------

1. Install the package via pip:

   ```bash
   pip install wagtail_optimizer
   ```

2. Add 'wagtail_optimizer' to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
    ...,
       'wagtail_optimizer',
    ]
    ```

3. Install Celery and configure it to work with your Django project.
   You can find more information on how to do this [here](http://docs.celeryproject.org/en/latest/django/index.html).

4. Check out the new "SEO" tab in your wagtail admin settings menu and get started with generating SEO reports for your pages.
