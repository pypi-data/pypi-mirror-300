from django.conf import settings
from .analyze.analyzers import DEFAULT_ANALYZERS

ANALYZERS = getattr(
    settings,
    "WAGTAIL_OPTIMIZER_ANALYZERS",
    DEFAULT_ANALYZERS,
)