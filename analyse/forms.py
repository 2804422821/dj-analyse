from django import forms
from .models import *
from django.forms import widgets


class EditAppForm(forms.ModelForm):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   choices=APP_TYPE, initial=2, required=True)

    class Meta:
        model = App
        fields = ('name', 'description', 'icon', 'type')
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control form-control-line'}),
            'description': widgets.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': widgets.FileInput(attrs={'class': 'form-control'}),
        }


class FieldForm(forms.ModelForm):
    type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   choices=FIELD_TYPE, initial=1, required=True)
    bind_key = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-line'}),
                               required=False)
    is_key = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   choices=YES_NO_TYPE, initial=False, required=True)
    default_show = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=YES_NO_TYPE, initial=True, required=True)

    class Meta:
        model = Field
        fields = {'name', 'is_key', 'bind_key', 'default_show', 'type'}
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control form-control-line'}),
        }
