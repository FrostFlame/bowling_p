from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from tournaments.models import Tournament, TYPE, TEAM_TYPE

class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'description', 'type', 'team_type', 'games', 'photo')
        widgets = {'photo': AdminResubmitImageWidget}

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название'}
        )
    )

    start = forms.DateTimeField(
        label='Начало',
        widget=forms.SelectDateWidget
    )

    end = forms.DateTimeField(
        label='Конец',
        widget=forms.SelectDateWidget
    )

    type = forms.ChoiceField(
        label='Тип турнира',
        choices=TYPE,
        required=False
    )

    team_type = forms.ChoiceField(
        label='Тип команд',
        choices=TEAM_TYPE,
        required=False
    )