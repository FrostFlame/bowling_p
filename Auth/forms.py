from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from django.core.exceptions import ValidationError
from file_resubmit.admin import AdminResubmitImageWidget

from Auth.models import User, PlayerInfo, SEX_CHOICES, CATEGORY_CHOICES


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Повторите пароль'}),
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


class PlayerRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        self.request = kwargs.pop('request', None)
        super(PlayerRegistrationForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={'placeholder': 'Имя'}),
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия'}),
    )
    patronymic = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Фамилия'}),
    )
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        required=False
    )
    phone = forms.CharField(
        label='Номер телефона',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Номер телефона'}),
    )
    date_of_birth = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1930, 2018),
            attrs={'placeholder': 'Дата рождения'}),
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False
    )

    class Meta:
        model = PlayerInfo
        fields = ('first_name', 'last_name', 'patronymic',
                  'sex', 'passport', 'phone',
                  'date_of_birth', 'license', 'category')
        widgets = {'passport': AdminResubmitImageWidget}

    def save(self, commit=True):
        player = super(PlayerRegistrationForm, self).save(commit=False)
        if commit:
            player.save()
        return player
