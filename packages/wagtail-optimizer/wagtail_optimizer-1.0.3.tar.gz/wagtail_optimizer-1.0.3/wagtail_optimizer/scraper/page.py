import bs4
import requests
from urllib.parse import urlparse, ParseResult
from datetime import datetime

from wagtail.models import (
    Page, Site,
)

from .tags import (
    AnchorTag,
    HeadingTag,
    ImageTag,
    get_css_selector,
)

def gettext(tag):
    if not tag:
        return ''
    
    if tag.text:
        return tag.text
    
    attrs = [
        'title', 'aria-label', 'alt',
    ]

    for attr in attrs:
        if tag.get(attr, None):
            return tag.get(attr)
    return ''

class PageScraper:
    def __init__(self, page: Page):
        self.page: Page = page
        self.page_url: ParseResult = urlparse(
            page.full_url,
        )
        
        start_time = datetime.now()
        response = requests.get(page.full_url)

        self.response_time = datetime.now() - start_time
        self.status_code = response.status_code
        self.soup = None
        
        if response.text:
            self.soup = bs4.BeautifulSoup(
                response.text, 'html.parser',
            )

    def to_json(self) -> dict:
        return self.page.id

    def to_json_expanded(self) -> dict:
        return {
            'id': self.page.id,
            'response_time': self.response_time.total_seconds(),
            'status_code': self.status_code,
        }

    def get_soup(self) -> bs4.BeautifulSoup | None:
        return self.soup
    
    def get_page(self) -> Page:
        return self.page
    
    def get_title(self) -> str | None:
        if not self.soup:
            return None
        
        title = self.soup.find('title')
        return title.text if title else None

    def get_meta_description(self) -> str | None:
        if not self.soup:
            return None
        
        description = self.soup.find('meta', attrs={'name': 'description'})
        return description.get('content', None) if description else None
    
    def get_meta_keywords(self) -> list[str] | None:
        if not self.soup:
            return None
        
        keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        kw = keywords.get('content', None) if keywords else None
        return list(map(str.strip, kw.split(','))) if kw else None

    def get_anchor_tags(self) -> list[AnchorTag]:
        if not self.soup:
            return []
        
        anchor_list: list[AnchorTag] = []
        for tag in self.soup.find_all('a'):
            tag: bs4.Tag

            anchor_list.append(AnchorTag(
                href=tag.get('href', ''),
                text=gettext(tag),
                url=urlparse(tag.get('href', '')),
                selector=get_css_selector(
                    tag,
                ),
            ))
            
        return anchor_list

    def get_heading_tags(self) -> list[HeadingTag]:
        if not self.soup:
            return []
        
        headings: list[bs4.Tag] = []
        for tag in self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            tag: bs4.Tag
            headings.append(tag)

        headings.sort(key=lambda tag: tag.sourceline)

        heading_list: list[HeadingTag] = []
        for tag in headings:
            heading_list.append(HeadingTag(
                selector=get_css_selector(
                    tag,
                ),
                tag=tag.name,
                text=tag.text,
            ))

        return heading_list

    def get_image_tags(self) -> list[ImageTag]:
        if not self.soup:
            return []
        
        image_list: list[ImageTag] = []
        for tag in self.soup.find_all('img'):
            tag: bs4.Tag
            image_list.append(ImageTag(
                selector=get_css_selector(
                    tag,
                ),
                src=tag.get('src', ''),
                alt=tag.get('alt', ''),
            ))
        return image_list
