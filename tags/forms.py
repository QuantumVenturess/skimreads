from django import forms
from django.forms import ModelForm
from tags.models import Tie

class TieForm(ModelForm):
    tag_name = forms.CharField(max_length=15, 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
        'placeholder': 'new tag', 'tabindex': 1 }))

    class Meta:
        model = Tie
        fields = ('tag_name',)