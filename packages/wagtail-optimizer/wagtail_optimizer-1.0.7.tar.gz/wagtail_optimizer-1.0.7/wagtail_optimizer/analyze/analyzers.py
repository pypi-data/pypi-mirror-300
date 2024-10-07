from collections import (
    defaultdict,
)
from django.utils.functional import classproperty
from django.utils.translation import (
    gettext_lazy as _,
)
import requests, logging
from .errors import (
    ERR_PAGE_LOAD,
    ERR_PAGE_4XX_STATUSCODE,
    ERR_PAGE_5XX_STATUSCODE,
    ERR_PAGE_NO_TITLE,
    ERR_PAGE_NO_DESCRIPTION,
    ERR_PAGE_NO_KEYWORDS,
    ERR_ANCHOR_NO_TEXT,
    ERR_ANCHOR_NO_HREF,
    ERR_PAGE_HEADING_NOT_H1,
    ERR_PAGE_DUPLICATE_H1,
    ERR_IMAGE_NO_ALT,
    ERR_IMAGE_NO_SRC,
    ERR_PAGES_DUPLICATE_TITLE,
    MultiPageError,
    MultiPageWarning,
    PageError,
    PageWarning,
)
from ..scraper import (
    PageScraper,
)

logger = logging.getLogger("wagtail_optimizer")

class AnalyzerRegistry:
    def __init__(self):
        self.analyzers = {}

    def register(self, analyzer: type["BaseAnalyzer"] = None, id: str = None):
        if id is None:
            id = analyzer.id
        
        if analyzer is None:
            def inner(analyzer):
                self.register(analyzer, id)
                return analyzer
            return inner
        
        self.analyzers[id] = analyzer

    def get_analyzer(self, id: str):
        return self.analyzers.get(id)

    def get_analyzers(self):
        return self.analyzers.values()

    def get_analyzer_choices(self):
        return [
            (analyzer.id, analyzer.title)
            for analyzer in self.get_analyzers()
        ]
    
registry = AnalyzerRegistry()

class BaseAnalyzer:
    id: str
    title: str
    description: str

    def __init__(self):
        self.single_page_errors: list[PageError] = []
        self.single_page_warnings: list[PageWarning] = []
        self.multi_page_errors: list[MultiPageError] = []
        self.multi_page_warnings: list[MultiPageWarning] = []
    
    def add_error(self, error_message: str, page: PageScraper, weight: int = 0.97, data: dict = None, descriptive_message: str = None):
        self.single_page_errors.append(PageError(
            analyzer=self,
            error_message=error_message,
            descriptive_message=descriptive_message,
            page=page,
            weight=weight,
            data=data,
        ))

    def add_warning(self, error_message: str, page: PageScraper, weight: int = 0.99, data: dict = None, descriptive_message: str = None):
        self.single_page_warnings.append(PageWarning(
            analyzer=self,
            error_message=error_message,
            descriptive_message=descriptive_message,
            page=page,
            weight=weight,
            data=data,
        ))

    def add_multi_error(self, error_message: str, pages: list[PageScraper], weight: int = 0.97, data: dict = None, descriptive_message: str = None):
        self.multi_page_errors.append(MultiPageError(
            analyzer=self,
            error_message=error_message,
            descriptive_message=descriptive_message,
            pages=pages,
            weight=weight,
            data=data,
        ))

    def add_multi_warning(self, error_message: str, pages: list[PageScraper], weight: int = 0.99, data: dict = None, descriptive_message: str = None):
        self.multi_page_warnings.append(MultiPageWarning(
            analyzer=self,
            error_message=error_message,
            descriptive_message=descriptive_message,
            pages=pages,
            weight=weight,
            data=data,
        ))

    def format_error_message(self, error_message: str, data: dict) -> str:
        return error_message
    
    def format_error_description(self, descriptive_message: str, data: dict) -> str:
        return descriptive_message

    def format_error_data(self, data: dict) -> list[tuple[str, str]]:
        datalist = []
        for key in data.keys():
            datalist.append(key)
        datalist.sort()
        
        lines = []
        for key in datalist:
            lines.append(
                (key.title(), data[key]),
            )
        return lines

    def to_json(self) -> dict:
        return {
            'id': self.id,
        }

    def analyze_page(self, page: PageScraper):
        pass

    def analyze(self, pages: list[PageScraper]):
        pass

class _WagtailOptimizerAnalyzer(BaseAnalyzer):
    @classproperty
    def id(cls):
        return f"wagtail_optimizer.analyze.analyzers.{cls.__name__}"

@registry.register
class TitleAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Title Analyzer")
    description = _("Analyze the titles of pages, looking for duplicates and missing titles")

    def analyze(self, pages: list[PageScraper]):
        duplicate_title_count = defaultdict(list)
        for page in pages:
            title = page.get_title()
            if title:
                duplicate_title_count[title].append(
                    page,
                )
            else:
                self.add_error(
                    error_message=ERR_PAGE_NO_TITLE,
                    page=page,
                    weight=0.9,
                )
        
        for title, page_list in duplicate_title_count.items():
            if len(page_list) > 1:
                self.add_multi_error(
                    error_message=ERR_PAGES_DUPLICATE_TITLE,
                    pages=page_list,
                    weight=0.9,
                    data={
                        'title': title,
                    }
                )

@registry.register
class DescriptionAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Description Analyzer")
    description = _("Analyze the meta description of pages, looking for missing descriptions")

    def analyze_page(self, page: PageScraper):
        description = page.get_meta_description()
        if not description:
            self.add_error(
                error_message=ERR_PAGE_NO_DESCRIPTION,
                page=page,
                weight=0.98,
            )


@registry.register
class KeywordsAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Keywords Analyzer")
    description = _("Analyze the meta keywords of pages, looking for missing keywords")

    def analyze_page(self, page: PageScraper):
        keywords = page.get_meta_keywords()
        if not keywords:
            self.add_warning(
                error_message=ERR_PAGE_NO_KEYWORDS,
                page=page,
            )


@registry.register
class AnchorAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Anchor Analyzer")
    description = _("Analyze the anchor tags of pages, looking for missing text and href")

    def analyze_page(self, page: PageScraper):
        anchor_tags = page.get_anchor_tags()
        for tag in anchor_tags:
            if not tag.text:
                self.add_warning(
                    error_message=ERR_ANCHOR_NO_TEXT,
                    page=page,
                    weight=0.97,
                    data={
                        'href': tag.href,
                        'selector': tag.selector,
                    }
                )
            
            if not tag.href:
                self.add_error(
                    error_message=ERR_ANCHOR_NO_HREF,
                    page=page,
                    weight=0.95,
                    data={
                        'text': tag.text,
                        'selector': tag.selector,
                    }
                )


@registry.register
class HeadingAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Heading Analyzer")
    description = _("Analyze the heading tags of pages, looking for missing text and tags")

    def analyze_page(self, page: PageScraper):
        heading_tags = page.get_heading_tags()
        heading_count = defaultdict(int)
        for i, tag in enumerate(heading_tags):
            heading_count[tag.tag] += 1
            
            if i == 0 and tag.tag != 'h1':
                self.add_error(
                    error_message=ERR_PAGE_HEADING_NOT_H1,
                    page=page,
                    weight=0.97,
                    data={
                        'tag': tag.tag,
                        'text': tag.text,
                        'selector': tag.selector,
                    },
                )
            
            if tag.tag == 'h1' and heading_count['h1'] > 1:
                self.add_error(
                    error_message=ERR_PAGE_DUPLICATE_H1,
                    page=page,
                    weight=0.95,
                    data={
                        'text': tag.text,
                        'selector': tag.selector,
                    },
                )

    def format_error_description(self, descriptive_message: str, data: dict) -> str:
        if "tag" not in data:
            return _("having multiple h1 tags is not recommended and might confuse search engines")
        
        return _("the first heading tag in the document should be an h1 tag")

@registry.register
class ImageAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Image Analyzer")
    description = _("Analyze the image tags of pages, looking for missing alt and src attributes")

    def analyze_page(self, page: PageScraper):
        image_tags = page.get_image_tags()
        for tag in image_tags:
            if not tag.alt:
                self.add_warning(
                    error_message=ERR_IMAGE_NO_ALT,
                    page=page,
                    data={
                        'src': tag.src,
                        'selector': tag.selector,
                    },
                )
            
            if not tag.src:
                self.add_error(
                    error_message=ERR_IMAGE_NO_SRC,
                    page=page,
                    weight=0.95,
                    data={
                        'alt': tag.alt,
                        'selector': tag.selector,
                    },
                )

    def format_error_data(self, data: dict) -> list[tuple[str, str]]:
        datalist = []
        if "alt" in data:
            datalist.append(
                (_("Alt"), data["alt"]),
            )
        if "src" in data:
            datalist.append(
                (_("Source"), data["src"]),
            )
        if "selector" in data:
            datalist.append(
                (_("Selector"), data["selector"]),
            )
        return datalist
    

@registry.register
class LoadTimeAnalyzer(_WagtailOptimizerAnalyzer):
    MAX_LOAD_TIME = 3
    title = _("Load Time Analyzer")
    description = _("Analyze the load time of pages, looking for pages that take too long to load")

    def analyze_page(self, page: PageScraper):
        total = page.response_time.total_seconds()
        if total > self.MAX_LOAD_TIME:
            self.add_error(
                error_message=ERR_PAGE_LOAD,
                page=page,
                weight=0.9,
                data={
                    'load_time': total,
                },
            )
    
    def format_error_data(self, data: dict) -> list[tuple[str, str]]:
        if "load_time" not in data:
            return []
        
        return [
            (_("Load Time"), _("%(load_time).2f seconds") % data),
        ]

class BaseMinifiedAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Minified Analyzer")
    description = _("Analyze the HTML of pages, looking for pages that have assets which have not been minified")
    SOUP_QUERY: tuple[str, dict] = ('html', {})
    SOUP_ATTR: str = 'src'
    ERROR_MESSAGE: str = ""
    DESCRIPTION: str = _("minified assets are recommended for better performance")
    MIN_CHARS: int = 450
    RATIO: float = 0.05

    def __init__(self):
        super().__init__()
        self.requests_pool = requests.Session()

    def is_minified(self, text: str) -> bool:
        newlines = text.count('\n')
        chars = len(text)

        if chars < self.MIN_CHARS:
            return True
        
        ratio = newlines / chars
        return ratio < self.RATIO

    def fetch_data(self, url: str) -> str:
        try:
            response = self.requests_pool.get(url)
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch data from %s: %s", url, e)
            return ''
        return response.text
    
    def analyze(self, pages: list[PageScraper]):
        is_minified_dict = {}
        asset_map = defaultdict(list)
        for page in pages:
            if not page.soup:
                continue

            tags = page.soup.find_all(
                *self.SOUP_QUERY,
            )
            for tag in tags:
                url = tag.get(self.SOUP_ATTR)
                if url:
                    asset_map[url].append(page)

        for url, page_list in asset_map.items():
            if url not in is_minified_dict:
                fetch_url = page.page_url\
                    ._replace(path=url)\
                    .geturl()
                
                data = self.fetch_data(fetch_url)
                if not data:
                    logger.warning("Empty response from %s", url)
                    return

                is_minified_dict[url] = self.is_minified(
                    data,
                )

            if not is_minified_dict[url]:
                self.add_multi_error(
                    error_message=self.ERROR_MESSAGE,
                    descriptive_message=self.DESCRIPTION,
                    pages=page_list,
                    weight=0.98,
                    data={
                        'source': url,
                    }
                )

    def format_error_data(self, data: dict) -> list[tuple[str, str]]:
        if "source" not in data:
            return []
        
        return [
            (_("Source"), data["source"]),
        ]
    
    def format_error_description(self, descriptive_message: str, data: dict) -> str:
        return self.DESCRIPTION

@registry.register
class CSSMinifiedAnalyzer(BaseMinifiedAnalyzer):
    ERROR_MESSAGE = _("CSS file is not minified")
    SOUP_QUERY = ('link', {'rel': 'stylesheet'})
    SOUP_ATTR = 'href'

@registry.register
class JSMinifiedAnalyzer(BaseMinifiedAnalyzer):
    ERROR_MESSAGE = _("JS file is not minified")
    SOUP_QUERY = ('script', {'src': True})
    SOUP_ATTR = 'src'
    RATIO = 0.025

@registry.register
class StatusCodeAnalyzer(_WagtailOptimizerAnalyzer):
    title = _("Status Code Analyzer")
    description = _("Analyze the status code of pages, looking for pages that return an error code")

    def analyze_page(self, page: PageScraper):
        if page.status_code >= 400 and page.status_code < 500:
            self.add_error(
                error_message=ERR_PAGE_4XX_STATUSCODE,
                page=page,
                weight=0.94,
                data={
                    'code': page.status_code,
                },
            )

        if page.status_code >= 500:
            self.add_error(
                error_message=ERR_PAGE_5XX_STATUSCODE,
                page=page,
                weight=0.94,
                data={
                    'code': page.status_code,
                },
            )

    def format_error_data(self, data: dict) -> list[tuple[str, str]]:
        if "code" not in data:
            return []
        
        return [
            (_("Status Code"), data["code"]),
        ]

DEFAULT_ANALYZERS = [
    obj.id for obj in registry.get_analyzers()
]