from django import forms
from .models import Template
# from django.contrib.auth Users

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'message', 'image']
