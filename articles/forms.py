from django import forms
from .models import Article
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCEWidget(attrs={'required': True, 'cols': 30, 'rows': 10}))

    class Meta:
        model = Article
        fields = ['title']
