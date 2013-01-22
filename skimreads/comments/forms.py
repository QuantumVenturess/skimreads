from django import forms
from django.forms import ModelForm, Textarea
from comments.models import Comment

class CommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))

    class Meta:
        model = Comment
        fields = ('content',)