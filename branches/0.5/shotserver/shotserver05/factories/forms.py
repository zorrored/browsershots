from django import forms
from shotserver05.factories.models import Factory


class FactoryForm(forms.ModelForm):
    secret_key = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    hardware = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    class Meta:
        model = Factory
        exclude = ('name', 'user')
