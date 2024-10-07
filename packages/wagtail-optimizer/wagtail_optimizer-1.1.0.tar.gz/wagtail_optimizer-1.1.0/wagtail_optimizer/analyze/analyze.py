from django.utils.translation import (
    gettext_lazy as _,
)
from ..scraper import (
    PageScraper,
)
from .errors import (
    MultiPageError,
    MultiPageWarning,
    PageError,
    PageWarning,
)

class Analysis:
    def __init__(self,
            multi_page_errors: list[MultiPageError],
            multi_page_warnings: list[MultiPageWarning],
            single_page_errors: list[PageError],
            single_page_warnings: list[PageWarning],
            scraped_pages: list[PageScraper],
        ):
        self.multi_page_errors = multi_page_errors
        self.multi_page_warnings = multi_page_warnings
        self.single_page_errors = single_page_errors
        self.single_page_warnings = single_page_warnings
        self.scraped_pages = scraped_pages

    def to_json(self) -> dict:
        return {
            'multi_page_errors': [
                error.to_json() for error in self.multi_page_errors
            ],
            'multi_page_warnings': [
                warning.to_json() for warning in self.multi_page_warnings
            ],
            'single_page_errors': [
                error.to_json() for error in self.single_page_errors
            ],
            'single_page_warnings': [
                warning.to_json() for warning in self.single_page_warnings
            ],
            'pages': [
                page.to_json_expanded() for page in self.scraped_pages
            ],
        }
