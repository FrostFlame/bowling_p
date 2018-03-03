from django import forms
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from file_resubmit.admin import AdminResubmitImageWidget

from news.models import News


class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'image', 'text')

    title = forms.CharField()

    image = forms.ImageField()

    text = forms.CharField(widget=SummernoteWidget())
