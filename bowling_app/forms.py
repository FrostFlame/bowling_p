from dal import autocomplete
from django import forms

from accounts.forms import RegisterUserForm
from accounts.models import PlayerInfo, SportCategory, SEX_CHOICES, City


class StaffPlayerRegister(forms.ModelForm):
    """ Форма создания игрока модератором """

    f_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    i_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Имя', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    o_name = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Отчество', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]*$'}),
    )
    sex = forms.ChoiceField(
        label='Пол',
        choices=SEX_CHOICES,
        required=False,
        initial=SEX_CHOICES[1],
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
            attrs={'placeholder': 'Дата рождения', 'autocomplete': 'off', 'class': 'form-control'}),
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
        initial=City.objects.first(),
        widget=autocomplete.ModelSelect2(url='bowlingApp:city-autocomplete',
                                         attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}),
    )

    class Meta:
        # fields = ()
        model = PlayerInfo
        exclude = ('user', 'passport', 'avatar')

    def save(self, commit=True):
        player = super(StaffPlayerRegister, self).save(commit=False)
        if commit:
            player.save()
        return player


class PlayerSearchForm(forms.Form):
    name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'ФИО игрока', 'class': 'form-control'}
        )
    )


class PersonalRegisterForm(RegisterUserForm):
    PERSONAL_CHOICES = (('1', 'Фотограф',), ('2', 'Редактор',))
    role = forms.ChoiceField(
        label='Роль',
        required=True,
        choices=PERSONAL_CHOICES,
    )
