from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

# Registration Form
class reg_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
