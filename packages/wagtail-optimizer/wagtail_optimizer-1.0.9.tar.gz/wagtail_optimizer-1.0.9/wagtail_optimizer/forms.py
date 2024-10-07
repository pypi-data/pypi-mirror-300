from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail.admin.rich_text import get_rich_text_editor_widget

class AnalysisForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=False,
        widget=forms.TextInput()
    )
    
    notes = forms.CharField(
        label=_("Notes"),
        required=False,
        widget=get_rich_text_editor_widget(
            features=[
                "bold", "italic", "link",
                "h2", "h3", "h4", "h5", "h6",
                "ol", "ul", "blockquote",
                "image", "document-link",
            ]
        )
    )
