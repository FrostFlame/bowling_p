from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from tournaments.models import Tournament, TYPE, TeamType


class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'description', 'type', 'team_type', 'games', 'photo')
        widgets = {'photo': AdminResubmitImageWidget}

    photo = forms.ImageField(
        label='Фото паспорта'
    )

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control'}
        )
    )

    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )

    games = forms.CharField(
        label='Количество игр',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    start = forms.DateTimeField(
        label='Начало',
        widget=forms.SelectDateWidget()
    )

    end = forms.DateTimeField(
        label='Конец',
        widget=forms.SelectDateWidget()
    )

    type = forms.ChoiceField(
        label='Тип турнира',
        choices=TYPE,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    team_type = forms.ModelChoiceField(
        label='Тип команд',
        queryset=TeamType.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
