from urllib.parse import ParseResult
import bs4


def get_css_selector(tag: bs4.Tag):
    if "id" in tag.attrs:
        return f"#{tag['id']}"
    if "class" in tag.attrs:
        return tag.name + "." + ".".join(tag['class'])

    path = []
    
    while tag and tag.name != 'html':
        selector = tag.name

        if 'id' in tag.attrs:
            selector += f"#{tag['id']}"
            path.insert(0, selector)
            break  # Stop since ID is unique
        elif 'class' in tag.attrs:
            selector += '.' + '.'.join(tag['class'])
        else:
            # Add nth-child if no id or class
            sibling_index = 1
            sibling = tag
            while sibling.previous_sibling:
                sibling = sibling.previous_sibling
                if sibling.name == tag.name:
                    sibling_index += 1
            selector += f":nth-child({sibling_index})"
        
        path.insert(0, selector)
        tag = tag.parent

    return ' > '.join(path)


class BaseSelectable:
    def __init__(self, selector: str = None):
        self.selector: str = selector

    def to_json(self) -> dict:
        attrs = vars(self)
        return {k: v for k, v in attrs.items() if not k.startswith('_')}

class AnchorTag(BaseSelectable):
    def __init__(self, selector: str, href: str, text: str, url: ParseResult):
        super().__init__(selector)
        self.href: str = href
        self.text: str = text
        self.url: ParseResult = url

    def to_json(self) -> dict:
        data = super().to_json()
        data['url'] = self.url.geturl()
        return data

class HeadingTag(BaseSelectable):
    def __init__(self, selector: str, tag: str, text: str):
        super().__init__(selector)
        self.tag: str = tag
        self.text: str = text

class ImageTag(BaseSelectable):
    def __init__(self, selector: str, src: str, alt: str):
        super().__init__(selector)
        self.src: str = src
        self.alt: str = alt

class AssetTag(BaseSelectable):
    def __init__(self, src: str, selector: str = None):
        super().__init__(selector)
        self.src: str = src