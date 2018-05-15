from dal import autocomplete
from django import forms
from django.forms import CheckboxSelectMultiple

from rating.models import Rating
from tournaments.models import Tournament


class RatingCreationForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RatingCreationForm, self).__init__(*args, **kwargs)

        self.fields["tournaments"].label = "Турниры"
        self.fields["tournaments"].widget = CheckboxSelectMultiple()
        self.fields["tournaments"].queryset = Tournament.objects.order_by('name')

    name = forms.CharField(
        label="Название",
        widget=forms.TextInput(
            attrs={'placeholder': 'Название', 'class': 'form-control'}
        )
    )

