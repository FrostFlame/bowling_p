from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from albums.models import Photo, Album
from tournaments.models import Tournament


class AddImagesForm(forms.ModelForm):

    class Meta:
        model=Photo
        fields=('image',)

    image = forms.ImageField(
        label='Фото',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            })
    )


class CreatAlbumForm(forms.ModelForm):

    class Meta:
        model=Album
        fields=('name','cover','tournament')

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[0-9a-zA-Zа-яёА-ЯЁ",.\\-\s№#\\(\\)\\–]+$'}
        )
    )

    cover = forms.ImageField(
        required=False,
        label='Обложка',
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control'}
        )
    )

    tournament = forms.ModelChoiceField(
        label='Привязать к турниру',
        queryset=Tournament.objects.filter(tournament_album=None),
        empty_label="Не привязывать",
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

