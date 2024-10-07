import itertools
from collections import OrderedDict
from django.db import models
from django.urls import path, include, reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.utils.translation import (
    gettext_lazy as _,
)
from wagtail.models import (
    Page,
)
from wagtail.admin.menu import (
    MenuItem,
)
from wagtail.admin.ui.tables import (
    Column,
    TitleColumn,
    DateColumn,
)
from wagtail.admin.views.generic.base import (
    WagtailAdminTemplateMixin,
    BaseObjectMixin,
    BaseListingView,
)
from wagtail import hooks
import json

from .analyze import (
    registry,
    BaseAnalyzer,
)
from .models import (
    Analysis,
)
from .tasks import (
    run_analyzer,
)
from .settings import (
    ANALYZERS,
)
from .forms import (
    AnalysisForm,
)
from .views import (
    get_progress,
)


class SEOReportsView(BaseListingView):
    template_name = "wagtail_optimizer/seo_reports.html"
    page_title = _("SEO Reports")
    page_subtitle = _("View your SEO reports")
    header_icon = "glasses"

    model = Analysis
    paginate_by = 10
    default_ordering = "-created_at"
    _show_breadcrumbs = True
    breadcrumbs_items = []
    columns = [
        TitleColumn("title", label=_("Title"), url_name="wagtail_optimizer:report"),
        Column("seo_score", label=_("SEO Score")),
        DateColumn("created_at", label=_("Created At")),
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_obj = context["page_obj"]
        object_list = page_obj.object_list

        reports_seo_scores = object_list\
            .values("created_at", "seo_score")
        
        reports_error_counts = object_list\
            .annotate(
                error_count=models.F("mpe_count") + models.F("spe_count"),
                warning_count=models.F("mpw_count") + models.F("spw_count"),
            )\
            .values("created_at", "error_count", "warning_count")
        
        latest_analysis = Analysis.objects.order_by(
            "-created_at",
        ).first()
        if latest_analysis:
            context["latest_analysis"] = {
                "label": _("SEO Score"),
                "title": latest_analysis.title if latest_analysis else "",
                "value": latest_analysis.seo_score if latest_analysis else 0,
            }
        context["header_action_url"] = reverse("wagtail_optimizer:crawl")
        context["header_action_label"] = _("Crawl")
        context["reports_seo_scores"] = list(
            reversed(reports_seo_scores),
        )
        context["reports_error_counts"] = list(
            reversed(reports_error_counts),
        )

        return context

    
class SEOCrawlView(WagtailAdminTemplateMixin, TemplateView):
    template_name = "wagtail_optimizer/seo_crawl.html"
    page_title = _("Generate SEO Report")
    page_subtitle = _("Crawl your pages for SEO issues")
    header_icon = "search"
    form_class = AnalysisForm

    def get_form(self, *args, **kwargs):
        return self.form_class(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def post(self, request):
        data = request.body.decode("utf-8")
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            data = {}

        form = self.get_form(
            data,
        )

        if form.is_valid():
            title = form.cleaned_data.get("title")
            notes = form.cleaned_data.get("notes")

            result = run_analyzer.delay(
                title=title,
                notes=notes,
                analyzers=ANALYZERS,
            )

            return JsonResponse({
                "task_id": result.id,
                "progress_url": reverse(
                    "wagtail_optimizer:progress",
                    kwargs={
                        "task_id": result.id,
                    },
                ),
            })
        
        return JsonResponse({
            "form_html": render_to_string(
                "wagtail_optimizer/partials/form_html.html",
                {"form": form},
                request=request,
            )
        }, status=400)


class SEOCheckView(BaseObjectMixin, WagtailAdminTemplateMixin, TemplateView):
    model = Analysis
    template_name = "wagtail_optimizer/seo_check.html"
    page_title = _("SEO Check")
    page_subtitle = _("Check the SEO of your pages")
    header_icon = "search"


class SEOReportView(BaseObjectMixin, WagtailAdminTemplateMixin, TemplateView):
    object: Analysis
    model = Analysis
    template_name = "wagtail_optimizer/seo_report.html"
    page_title = _("SEO Report")
    page_subtitle = _("View the results of your SEO analysis report")
    _show_breadcrumbs = True
    breadcrumbs_items = WagtailAdminTemplateMixin.breadcrumbs_items + [
        {
            "url": reverse_lazy("wagtail_optimizer:reports"),
            "label": _("All Reports"),
        },
    ]
    header_icon = "search"

    def get_page_title(self):
        return _("SEO Report (%(date)s)") % {
            "date": self.object.created_at.strftime(
                "%H:%M %d-%m-%Y",
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["analysis"] = self.object

        page_ids = []
        for scraper in self.object.pages:
            if "id" not in scraper:
                continue

            page_ids.append(
                scraper["id"],
            )

        if not page_ids:
            return context

        pages = Page.objects.in_bulk(
            page_ids,
        )

        pages_with_data = OrderedDict()
        for page in pages:
            page: Page
            pages_with_data[page] = {
                "page": pages[page],
                "errors": [],
                "warnings": [],
            }

        for error in self.object.single_page_errors:            
            if error["page"] in pages_with_data:
                pages_with_data[error["page"]]["errors"].append(
                    error,
                )

        for warning in self.object.single_page_warnings:
            if warning["page"] in pages_with_data:
                pages_with_data[warning["page"]]["warnings"].append(
                    warning,
                )
                
        for error in self.object.multi_page_errors:
            for page in error["pages"]:
                if page not in pages_with_data:
                    continue

                pages_with_data[page]["errors"].append(
                    error,
                )

        for warning in self.object.multi_page_warnings:
            for page in warning["pages"]:
                if page not in pages_with_data:
                    continue

                pages_with_data[page]["warnings"].append(
                    warning,
                )

        for page, data in pages_with_data.items():
            for error in itertools.chain(
                data["errors"], data["warnings"],
            ):
                if "analyzer" in error \
                    and not isinstance(error["analyzer"], BaseAnalyzer) \
                    and "id" in error["analyzer"]:
                    
                    analyzer: BaseAnalyzer = registry.get_analyzer(
                        error["analyzer"]["id"],
                    )
                    error["analyzer"] = analyzer()

        values = list(pages_with_data.values())
        values.sort(
            key=lambda x:
                len(x["errors"]) + len(x["warnings"]),
            reverse=True,
        )

        context["pages"] = values
        return context


@hooks.register('register_admin_urls')
def register_wagtail_optimizer_urls():
    urls = [
        path('', SEOReportsView.as_view(), name='reports'),
        path('crawl/', SEOCrawlView.as_view(), name='crawl'),
        path('report/<int:pk>/', SEOReportView.as_view(), name='report'),
        path('progress/<uuid:task_id>/', get_progress, name='progress'),
    ]

    return [
        path('seo/', include(
            (urls, 'wagtail_optimizer'),
            namespace='wagtail_optimizer',
        ),
        name="wagtail_optimizer"),
    ]

@hooks.register('register_settings_menu_item')
def register_seo_reports_menu_item():
    return MenuItem(
        label=_("SEO Reports"),
        url=reverse('wagtail_optimizer:reports'),
        icon_name='site',
        order=1000,
    )
