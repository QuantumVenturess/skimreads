from django import forms
from django.forms import ModelForm
from usermessages.models import UserMessage

class NewMessageForm(ModelForm):
    content = forms.CharField(label='Message', 
        widget=forms.Textarea(attrs={
            'autocomplete': 'off',
            'placeholder': 'Message',
            'tabindex': 2 }))
    to = forms.CharField(label='To', 
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'id': 'to',
            'maxlength': 30,
            'placeholder': 'To',
            'tabindex': 1 }))

    class Meta:
        model = UserMessage
        fields = ('to', 'content')

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Why send a message with no message?')
        return content

    def clean_to(self):
        to = self.cleaned_data.get('to')
        if not to:
            raise forms.ValidationError('Do you want us to read your mind?')
        return to

class ReplyMessageForm(ModelForm):
    content = forms.CharField(label='Message', 
        widget=forms.Textarea(attrs={
            'autocomplete': 'off',
            'placeholder': 'Message' }))

    class Meta:
        model = UserMessage
        fields = ('content',)