from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

from wagtail.snippets.models import (
    register_snippet,
)
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
)

from .json import (
    WagtailOptimizerJSONEncoder,
    ExpandedWagtailOptimizerJSONEncoder,
)

# Create your models here.
class Analysis(models.Model):

    title = models.CharField(
        max_length=255,
    )
    notes = RichTextField(
        features=[
            "bold", "italic", "link",
            "h2", "h3", "h4", "h5", "h6",
            "ol", "ul", "blockquote",
            "image", "document-link",
        ],
        blank=True,
        null=True
    )
    multi_page_errors = models.JSONField(
        encoder=WagtailOptimizerJSONEncoder,
        blank=True,
        null=True
    )
    multi_page_warnings = models.JSONField(
        encoder=WagtailOptimizerJSONEncoder,
        blank=True,
        null=True
    )
    single_page_errors = models.JSONField(
        encoder=WagtailOptimizerJSONEncoder,
        blank=True,
        null=True
    )
    single_page_warnings = models.JSONField(
        encoder=WagtailOptimizerJSONEncoder,
        blank=True,
        null=True
    )
    pages = models.JSONField(
        encoder=ExpandedWagtailOptimizerJSONEncoder,
        blank=True,
        null=True
    )

    mpe_count = models.IntegerField(
        default=0,
        verbose_name=_("Multi-Page Errors"),
    )
    mpw_count = models.IntegerField(
        default=0,
        verbose_name=_("Multi-Page Warnings"),
    )
    spe_count = models.IntegerField(
        default=0,
        verbose_name=_("Single-Page Errors"),
    )
    spw_count = models.IntegerField(
        default=0,
        verbose_name=_("Single-Page Warnings"),
    )
    p_count = models.IntegerField(
        default=0,
        verbose_name=_("Pages Analyzed Count"),
    )

    seo_score = models.DecimalField(
        default=100,
        verbose_name=_("SEO Score"),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        decimal_places=2,
        max_digits=5,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("notes"),
        FieldPanel("created_at", read_only=True),
        FieldRowPanel([
            FieldPanel("mpe_count", read_only=True),
            FieldPanel("mpw_count", read_only=True),
        ]),
        FieldRowPanel([
            FieldPanel("spe_count", read_only=True),
            FieldPanel("spw_count", read_only=True),
        ]),
        FieldRowPanel([
            FieldPanel("p_count", read_only=True),
            FieldPanel("seo_score", read_only=True),
        ]),
        FieldPanel("multi_page_errors", read_only=True),
        FieldPanel("multi_page_warnings", read_only=True),
        FieldPanel("single_page_errors", read_only=True),
        FieldPanel("single_page_warnings", read_only=True),
        FieldPanel("pages", read_only=True),
    ]

    class Meta:
        verbose_name = _("Analysis")
        verbose_name_plural = _("Analyses")
        ordering = ("-created_at",)

    def __str__(self):
        if self.title:
            return self.title
        
        return f"{_('Analysis')} {self.id}"
        
    def save(self, *args, **kwargs):
        self.mpe_count = len(self.multi_page_errors)
        self.mpw_count = len(self.multi_page_warnings)
        self.spe_count = len(self.single_page_errors)
        self.spw_count = len(self.single_page_warnings)
        self.p_count = len(self.pages)
        super().save(*args, **kwargs)
