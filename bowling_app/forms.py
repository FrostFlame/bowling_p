from dal import autocomplete
from django import forms

from accounts.models import PlayerInfo, SportCategory, SEX_CHOICES, City
from bowling_app.models import Event


class StaffPlayerRegister(forms.ModelForm):
    i_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Имя', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    f_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    o_name = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    # avatar = forms.ImageField(
    #     label='Аватар',
    #     widget=AdminResubmitImageWidget(
    #         attrs={'class': 'form-control'}
    #     )
    # )
    sex = forms.ChoiceField(
        label='Пол',
        choices=SEX_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}, )
    )
    phone = forms.CharField(
        label='Номер телефона',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Номер телефона', 'class': 'form-control'}),
    )
    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Дата рождения', 'class': 'form-control'}),
    )
    category = forms.ModelChoiceField(
        label='Разряд',
        queryset=SportCategory.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control'}, )
    )
    license = forms.CharField(
        label='Номер лицензии',
        required=False,
        widget=forms.TextInput(
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

    class Meta:
        model = PlayerInfo
        exclude = ('user', 'passport', 'avatar')

    def save(self, commit=True):
        player = super(StaffPlayerRegister, self).save(commit=False)
        if commit:
            player.save()
        return player

class EventCreationForm (forms.ModelForm):

    name = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    date = forms.DateTimeField(
        label='Время мероприятия',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})$'}
        )
    )

    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        )
    )

    class Meta:
        model=Event
        fields=('name','date','description')
