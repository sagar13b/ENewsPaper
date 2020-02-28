from django import forms
from editor.models import NewsPost

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        #fields = '__all__'#('title', 'summary', 'body' )#'__all__'
        exclude = ('editor_detail',)
