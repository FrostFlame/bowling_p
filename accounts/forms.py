from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from django.core.exceptions import ValidationError
from file_resubmit.admin import AdminResubmitImageWidget

from accounts.models import User, PlayerInfo, SEX_CHOICES, SportCategory, City


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email', 'class': 'form-control', 'data-validation': 'email'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Пароль', 'class': 'form-control', 'data-validation': 'strength',
                   'data-validation-strength': '2'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Повторите пароль', 'class': 'form-control', 'data-validation': 'confirmation',
                   'data-validation-confirm': 'password'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password']

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        user.email_confirmed = False

        if commit:
            user.save()

        return user


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        super().error_messages['invalid_login'] = "Неправильный email или пароль."


class PlayerRegistrationForm(forms.ModelForm):
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
    passport = forms.ImageField(
        label='Фотография паспорта',
        required=True,
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control'}
        )
    )
    avatar = forms.ImageField(
        label='Аватар',
        widget=AdminResubmitImageWidget(
            attrs={'class': 'form-control'}
        )
    )
    o_name = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Отчество', 'class': 'form-control', 'data-validation': 'custom',
                   'data-validation-regexp': '^[a-zA-Zа-яА-Я]+$'}),
    )
    sex = forms.ChoiceField(
        label='Пол',
        choices=SEX_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}, )
    )
    phone = forms.CharField(
        label='Номер телефона',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Номер телефона', 'class': 'form-control'}),
    )
    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=True,
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
        exclude = ('user',)
        widgets = {'passport': AdminResubmitImageWidget, 'avatar': AdminResubmitImageWidget}

    def save(self, commit=True):
        player = super(PlayerRegistrationForm, self).save(commit=False)
        if commit:
            player.save()
        return player
