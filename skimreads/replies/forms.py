from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from replies.models import Reply

class AdminReplyForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Reply' }))
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('date_joined'))
    
    class Meta:
        model = Reply
        fields = ('content', 'user',)

class ReplyForm(ModelForm):
    content = forms.CharField(label='Content', 
        widget=forms.Textarea(attrs={ 'placeholder': 'Reply' }))
    
    class Meta:
        model = Reply
        fields = ('content',)