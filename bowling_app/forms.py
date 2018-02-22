from django import forms
from file_resubmit.admin import AdminResubmitImageWidget

from accounts.models import PlayerInfo, SportCategory, SEX_CHOICES, City


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
    avatar = forms.ImageField(
        label='Аватар',
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control'}
        )
    )
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

        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = PlayerInfo
        exclude = ('user', 'passport')

    def save(self, commit=True):
        player = super(StaffPlayerRegister, self).save(commit=False)
        if commit:
            player.save()
        return player
