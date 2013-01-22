from django import forms
from django.forms import ModelForm, Textarea
from replies.models import Reply

class ReplyForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Reply' }))
    
    class Meta:
        model = Reply
        fields = ('content',)