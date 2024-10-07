from django.http import HttpResponse
from django.views.decorators.cache import (
    never_cache,
)
from celery.result import AsyncResult
import json

from .progress import Progress


@never_cache
def get_progress(request, task_id):
    progress = Progress(
        AsyncResult(task_id),
    )

    return HttpResponse(
        json.dumps(progress.get_info()),
        content_type='application/json',
    )