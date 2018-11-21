from dal import autocomplete
from django import forms
from django_select2.forms import Select2MultipleWidget
from file_resubmit.admin import AdminResubmitImageWidget

from accounts.models import City, SEX_CHOICES
from tournaments.models import Tournament, TournamentType, TeamType, Game, BlockType, Block, Handicap


class TournamentCreationForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = (
            'name', 'start', 'end', 'description', 'type', 'team_type', 'block_type', 'handicaps', 'city', 'photo')

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
            attrs={'class': 'form-control vertical-resize', 'rows': '4'}
        )
    )

    start = forms.DateTimeField(
        label='Начало',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom, compare',
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
        initial=TournamentType.objects.first(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    team_type = forms.ModelMultipleChoiceField(
        label='Тип команд',
        queryset=TeamType.objects,
        initial=TeamType.objects.first(),
        widget=forms.CheckboxSelectMultiple
    )

    handicaps = forms.ModelMultipleChoiceField(
        label='Гандикап',
        queryset=Handicap.objects,
        initial=Handicap.objects.first(),
        widget=Select2MultipleWidget
    )

    block_type = forms.ModelChoiceField(
        empty_label=None,
        label='Блоки или этапы',
        queryset=BlockType.objects.all()
    )

    city = forms.ModelChoiceField(
        label='Город',
        queryset=City.objects.all(),
        empty_label=None,
        required=True,

        widget=autocomplete.ModelSelect2(url='bowlingApp:city-autocomplete',
                                         attrs={'class': 'form-control'})
    )


class HandicapCreationForm(forms.ModelForm):
    class Meta:
        model = Handicap
        fields = ('start', 'end', 'gender', 'size')

    start = forms.IntegerField()
    end = forms.IntegerField()
    gender = forms.ChoiceField(
        label='Пол',
        choices=SEX_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}, )
    )
    size = forms.IntegerField()


class GameCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'block' in kwargs:
            self.block = kwargs.pop('block')
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

    def save(self, commit=True):
        game = super(GameCreationForm, self).save(commit=False)
        if commit:
            game.date = self.cleaned_data['start'].date()
            game.time = self.cleaned_data['start'].time()
            game.block = self.block
            game.save()
        return game

    class Meta:
        model = Game
        exclude = ('date', 'time', 'block', 'info')


class BlockCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # if 'tournament_pk' in kwargs:
        #     self.tournament = kwargs.pop('tournament_pk')
        super(BlockCreationForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control'}
        )
    )

    start_date = forms.DateTimeField(
        label='Начало',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom, compare',
                   'data-validation-regexp': '^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$'}
        )
    )

    end_date = forms.DateTimeField(
        label='Конец',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom, compare',
                   'data-validation-regexp': '^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$'}
        )
    )

    description = forms.CharField(
        label="Описание",
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control vertical-resize', 'rows': '4'}
        )
    )
    is_final = forms.BooleanField(
        label='Финал',
        required=False
    )

    def save(self, commit=True):
        block = super(BlockCreationForm, self).save(commit=False)
        if commit:
            if not hasattr(block, 'tournament'):
                block.tournament = self.tournament
            block.save()
        return block

    class Meta:
        model = Block
        exclude = ('tournament', 'creation_date', 'players')


class TournamentSearchForm(forms.Form):
    search_field = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите название турнира или город', 'class': 'form-control'}
        )
    )
