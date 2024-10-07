from typing import TYPE_CHECKING, Literal, Mapping, Union

from django.utils.translation import (
    gettext_lazy as _,
)
from wagtail.models import Page

if TYPE_CHECKING:
    from ..scraper import BaseSelectable, PageScraper
    from .analyzers import BaseAnalyzer

ERR_SCRAPIG_PAGE = _("Error scraping page.")

ERR_PAGE_NO_TITLE = _("No title found.")
ERR_PAGE_HEADING_NOT_H1 = _("First heading tag is not an h1.")
ERR_PAGE_DUPLICATE_H1 = _("Duplicate h1 tag found.")
ERR_PAGE_LOAD = _("Page took too long to load.")
ERR_PAGE_4XX_STATUSCODE = _("Page returned a client error status code..")
ERR_PAGE_5XX_STATUSCODE = _("Page returned a server error status code..")
ERR_PAGE_NO_DESCRIPTION = _("No meta description found.")
ERR_PAGE_NO_KEYWORDS = _("No meta keywords found.")

ERR_IMAGE_NO_ALT = _("Image tag has no alt text.")
ERR_IMAGE_NO_SRC = _("Image tag has no src.")
ERR_ANCHOR_NO_TEXT = _("Anchor tag has no text.")
ERR_ANCHOR_NO_HREF = _("Anchor tag has no href.")

ERR_PAGES_DUPLICATE_TITLE = _("Identical title found on multiple pages.")

class BaseError:
    def __init__(self,
            error_message: str,
            analyzer: Union["BaseAnalyzer", None] = None,
            weight: int = 0.99,
            data: dict = None,
            descriptive_message: str = None,
        ):
        self.analyzer = analyzer
        self.error_message = error_message
        self.descriptive_message = descriptive_message
        self.weight = weight
        if data is None:
            data = {}
        self.data = data

    def to_json(self) -> dict:
        attrs = vars(self)
        return {k: v for k, v in attrs.items() if not k.startswith('_')}
    
class BasePageError(BaseError):
    def __init__(self,
            analyzer: "BaseAnalyzer",
            error_message: str,
            page: "PageScraper" = None,
            weight: int = 0.99,
            data: dict = None,
            descriptive_message: str = None,
        ):
        super().__init__(
            analyzer=analyzer, error_message=error_message,
            weight=weight, data=data,
            descriptive_message=descriptive_message,
        )
        self.page = page

class BaseMultiPageError(BaseError):
    def __init__(self,
            error_message: str,
            pages: list["PageScraper"],
            analyzer: "BaseAnalyzer" = None,
            weight: int = 0.99,
            data: dict = None,
            descriptive_message: str = None,
        ):
        super().__init__(
            analyzer=analyzer,
            error_message=error_message,
            weight=weight, data=data,
            descriptive_message=descriptive_message,
        )
        self.pages = pages

class PageError(BasePageError):
    pass

class PageWarning(BasePageError):
    pass

class MultiPageError(BaseMultiPageError):
    pass

class MultiPageWarning(BaseMultiPageError):
    pass
