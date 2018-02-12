from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from tournaments.models import Tournament, TYPE, TeamType, Game


class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'description', 'type', 'team_type', 'games', 'photo')
        widgets = {'photo': AdminResubmitImageWidget}

    photo = forms.ImageField(
        label='Изображение',
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control'}
        )
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
        initial='6',
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'min': '1', 'max': '99'}
        )
    )

    start = forms.DateTimeField(
        label='Начало',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    end = forms.DateTimeField(
        label='Конец',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
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


class GameCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'tournament' in kwargs:
            self.tournament = kwargs.pop('tournament')
        super(GameCreationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(label='Название',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Название', 'class': 'form-control'}
                           ))
    start = forms.DateTimeField(label='Время начала',
                                widget=forms.DateTimeInput)

    # tournament = forms.ModelChoiceField(queryset=Tournament.objects.all(),
    #                                     widget=autocomplete.ModelSelect2(url='tournaments:tournament-autocomplete'))

    def save(self, commit=True):
        game = super(GameCreationForm, self).save(commit=False)
        if commit:
            game.tournament = self.tournament
            game.save()
        return game

    class Meta:
        model = Game
        exclude = ('tournament', 'players')
