from admins.utils import admin_david_list, admin_user_list
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from comments.models import Comment

class AdminCommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))
    user = forms.ModelChoiceField(
        queryset=admin_user_list())

    class Meta:
        model = Comment
        fields = ('content', 'user',)

class DavidCommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))
    user = forms.ModelChoiceField(
        queryset=admin_david_list())

    class Meta:
        model = Comment
        fields = ('content', 'user',)

class CommentForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Comment' }))

    class Meta:
        model = Comment
        fields = ('content',)