import logging
import itertools
from celery import (
    Task,
    shared_task,
    states,
)
from django.urls import reverse
from django.conf import settings
from django.utils.translation import (
    gettext_lazy as _,
)
from wagtail.models import (
    Page,
)

from .scraper import (
    PageScraper,
)
from .analyze import (
    errors,
    BaseAnalyzer,
    DEFAULT_ANALYZERS,
    registry,
)
from .models import (
    Analysis as StoredAnalysis,
)
from .progress import (
    ProgressRecorder,
)

logger = logging.getLogger("wagtail_optimizer")

from celery.signals import task_postrun


@task_postrun.connect(retry=True)
def task_postrun_handler(**kwargs):
    """Runs after a task has finished. This will update the result backend to include the IGNORED result state.

    Necessary for HTTP to properly receive ignored task event."""
    if kwargs.pop('state') == states.IGNORED:
        task = kwargs.pop('task')
        task.update_state(state=states.IGNORED, meta=str(kwargs.pop('retval')))


@shared_task(name="wagtail_optimizer.tasks.run_analyzer", bind=True)
def run_analyzer(task: Task, title: str = None, notes: str = None, analyzers=None):

    # STEP 1: Collect all pages
    pages = Page.objects.all()\
        .defer_streamfields()\
        .live()\
        .public()\
        .select_related("locale")
    
    progress = ProgressRecorder(task)
    
    # Setup title / notes for the stored report.
    if not title:
        count = StoredAnalysis.objects.count()
        title = f"{_('Analysis')} {count + 1}"

    if not notes:
        notes = _("System generated SEO report")

    # Setup vars to generate a report
    scraped_pages: list[PageScraper] = []
    multi_page_errors = []

    progress.set_progress(
        0,
        len(pages),
        _("Scraping pages"),
    )

    # STEP 2: Scrape all pages
    # Scrape all pages to generate a report later on
    for i, page in enumerate(pages):
        page: Page

        locale = page.locale
        if locale and settings.USE_I18N:
            locale = locale.language_code
        else:
            locale = settings.LANGUAGE_CODE or _("default")

        progress.increment_progress(
            description=_("Scraping page %(page)s (%(locale)s)") % {
                "page": page,
                "locale": locale,
            },
        )

        try:
            scraper = PageScraper(page)
            scraped_pages.append(scraper)
        except Exception as e:
            multi_page_errors.append(
                errors.MultiPageError(
                    error_message= errors.ERR_SCRAPIG_PAGE,
                    pages=[page],
                    data={
                        "error": str(e),
                    },
                )
            )
        
    # STEP 3: Setup Analyzers
    # Import all analyzers
    if not analyzers:
        analyzers = DEFAULT_ANALYZERS
    
    analyzers: list[BaseAnalyzer] = list(map(
        registry.get_analyzer,
        analyzers,
    ))

    # Initialize all analyzers
    for i, analyzer in enumerate(analyzers):
        analyzers[i] = analyzer()

    progress.set_progress(
        0,
        len(analyzers) * len(scraped_pages),
        _("Analyzing pages"),
    )

    # STEP 4: Analyze all pages
    # Analyze all pages
    for page in scraped_pages:
        page: PageScraper

        for analyzer in analyzers:

            progress.increment_progress(
                description=_("Analyzing pages"),
            )
            analyzer.analyze_page(
                page,
            )

    progress.set_progress(
        0,
        len(analyzers) + 2,
        _("Re-analyzing pages"),
    )

    # STEP 5: Re-Analyze all pages
    # Re-Analyze all pages
    for analyzer in analyzers:
        progress.increment_progress(
            description=_("Analyzing pages"),
        )
        analyzer.analyze(scraped_pages)

    # STEP 6: Collect all errors and warnings
    # Collect all errors and warnings
    single_page_warnings: list[errors.BaseError] = []
    single_page_errors: list[errors.BaseError] = []

    multi_page_warnings: list[errors.MultiPageError] = []
    multi_page_errors: list[errors.MultiPageError] = []

    for analyzer in analyzers:
        single_page_warnings.extend(analyzer.single_page_warnings)
        single_page_errors.extend(analyzer.single_page_errors)
        multi_page_warnings.extend(analyzer.multi_page_warnings)
        multi_page_errors.extend(analyzer.multi_page_errors)

    progress.increment_progress(
        description=_("Calculating SEO score"),
    )

    # STEP 7: Calculate SEO score
    # Calculate SEO score
    seo_score = 100
    for error in itertools.chain(
        multi_page_errors, single_page_errors,
        multi_page_warnings, single_page_warnings,
    ):
        seo_score *= error.weight

    progress.increment_progress(
        description=_("Storing analysis"),
    )

    # STEP 8: Store the analysis report
    # Store the analysis
    stored = StoredAnalysis.objects.create(
        title=title,
        notes=notes,
        multi_page_errors=multi_page_errors,
        multi_page_warnings=multi_page_warnings,
        single_page_errors=single_page_errors,
        single_page_warnings=single_page_warnings,
        pages=scraped_pages,
        seo_score=seo_score,
    )

    # Return a summary of the analysis
    return {
        "title": stored.title,
        "result_url": reverse(
            "wagtail_optimizer:report",
            kwargs={
                "pk": stored.pk,
            },
        ),
        "multi_page_errors_count": len(stored.multi_page_errors),
        "multi_page_warnings_count": len(stored.multi_page_warnings),
        "single_page_errors_count": len(stored.single_page_errors),
        "single_page_warnings_count": len(stored.single_page_warnings),
        "pages": len(stored.pages),
    }