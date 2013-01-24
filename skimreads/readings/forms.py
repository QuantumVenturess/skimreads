from django import forms
from django.forms import ModelForm, TextInput
from django.forms.formsets import BaseFormSet
from readings.models import Note, Reading

class ReadingForm(ModelForm):
    link = forms.CharField(label='Page URL', 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'placeholder': "Copy URL from the page you're reading and paste here" }))
    title = forms.CharField(label='Title', 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'placeholder': 'Enter a title for your reading',
            'maxlength': 80 }))
    image = forms.CharField(label='Image URL', required=False, 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'placeholder': 'Click on an image to attach it with this reading' }))

    class Meta:
        model = Reading
        fields = ('link', 'title', 'image')

class EditReadingForm(ModelForm):
    link = forms.CharField(label='Page URL', 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'readonly': 'readonly' }))
    title = forms.CharField(label='Title', 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'readonly': 'readonly' }))
    image = forms.CharField(label='Image URL', required=False,
        widget=forms.TextInput(attrs={ 'autocomplete': 'off', 
            'placeholder': 'Click on an image to attach it with this reading' }))
    
    class Meta:
        model = Reading
        fields = ('link', 'title', 'image')

class NoteForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'maxlength': 120, 
            'placeholder': 'Add your note here' }))

    class Meta:
        model = Note
        fields = ('content',)

    def clean_content(self):
        """Check to see if note content is blank."""
        error_message = 'Note cannot be blank'
        content = self.cleaned_data['content']
        if not content.strip():
            raise forms.ValidationError(error_message)
        return content

class RequiredFormSet(BaseFormSet):
    """Require non empty forms in a formset."""
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms[:1]:
            form.empty_permitted = False