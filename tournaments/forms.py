from dal import autocomplete
from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from accounts.models import City
from tournaments.models import Tournament, TournamentType, TeamType, Game


class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'description', 'type', 'team_type', 'city', 'photo')

    photo = forms.ImageField(
        required=False,
        label='Изображение',
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control', 'data-validation': 'mime size', 'data-validation-allowing': 'jpg, png, gif',
                   'data-validation-max-size': '20Mb',
                   'data-validation-error-msg-size': 'Вы не можете загружать изображения больше 20Мб',
                   'data-validation-error-msg-mime': 'Вы можете загружать только изображения.'}
        )
    )

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[0-9a-zA-Zа-яёА-ЯЁ",.\\-\s№#\\(\\)\\–]+$'}
        )
    )

    description = forms.CharField(
        label="Описание",
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        )
    )

    start = forms.DateTimeField(
        label='Начало',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$'}
        )
    )

    end = forms.DateTimeField(
        label='Конец',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom, compare',
                   'data-validation-regexp': '^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$'}
        )
    )

    type = forms.ModelChoiceField(
        label='Тип турнира',
        queryset=TournamentType.objects.all(),
        empty_label=None,
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

    city = forms.ModelChoiceField(
        label='Город',
        queryset=City.objects.all(),
        empty_label=None,
        required=True,

        widget=autocomplete.ModelSelect2(url='bowlingApp:city-autocomplete',
                                         attrs={'class': 'form-control'})
    )


class GameCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'tournament' in kwargs:
            self.tournament = kwargs.pop('tournament')
        super(GameCreationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control'}
        )
    )
    start = forms.DateTimeField(
        label='Время начала',
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control'}
        )
    )

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

class TournamentSearchForm(forms.Form):
    name = forms.CharField(
            label='Название',
            required=False,
            widget=forms.TextInput(
                attrs={'class': 'form-control'}
            )
        )
    city = forms.ModelChoiceField(
        label='Город',
        queryset=City.objects.all(),
        empty_label=None,
        required=False,
        widget=autocomplete.ModelSelect2(url='bowlingApp:city-autocomplete',
                                         attrs={'class': 'form-control'})
    )
