from django import forms

from events.models import Event


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
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        )
    )

    class Meta:
        model = Event
        fields = ('name', 'date', 'description',)
