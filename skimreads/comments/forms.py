from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from comments.models import Comment

class AdminCommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('date_joined'))

    class Meta:
        model = Comment
        fields = ('content', 'user',)

class CommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))

    class Meta:
        model = Comment
        fields = ('content',)