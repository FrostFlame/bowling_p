from django import forms
from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from file_resubmit.admin import AdminResubmitImageWidget

from news.models import News


class NewsCreationForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'image', 'text')

    title = forms.CharField(
        label='Заголовок',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    image = forms.ImageField(
        label='Обложка'
    )

    text = forms.CharField(
        label='Содержимое',
        widget=SummernoteWidget(
            attrs={'width': '100%'}
        )
    )
