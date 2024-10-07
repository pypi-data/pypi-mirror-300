from django.template import library
from ..analyze import (
    errors,
    BaseAnalyzer,
)

register = library.Library()

@register.simple_tag(name="format_error_message")
def format_error_message(error) -> str:
    analyzer = error.get("analyzer", None)
    if analyzer is None:
        return error.get("error_message", "")
    
    analyzer: BaseAnalyzer
    message = error.get("error_message", "")
    data = error.get("data", {})

    return analyzer.format_error_message(
        error_message=message,
        data=data,
    )

@register.simple_tag(name="format_error_description")
def format_error_description(error) -> str:
    analyzer = error.get("analyzer", None)
    if analyzer is None:
        return error.get("descriptive_message", "")
    
    analyzer: BaseAnalyzer
    message = error.get("descriptive_message", "")
    data = error.get("data", {})

    return analyzer.format_error_description(
        descriptive_message=message,
        data=data,
    )


@register.simple_tag(name="format_error_data")
def format_error_data(error) -> list[tuple[str, str]]:
    analyzer = error.get("analyzer", None)
    if analyzer is None:
        return []
    
    analyzer: BaseAnalyzer
    if "data" in error:
        return analyzer.format_error_data(
            error["data"],
        )
    
    return []
    