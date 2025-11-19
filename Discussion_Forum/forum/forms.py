from django import forms
from .models import Thread, Comment

# Thread Form
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})}