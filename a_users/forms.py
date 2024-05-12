from django.forms import ModelForm
from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image' : forms.FileInput(),
            'bio' : forms.Textarea(attrs={'rows' : 3}),
        }
