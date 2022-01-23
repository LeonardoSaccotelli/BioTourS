from django import forms
from django.forms import ModelForm
from .models import Sighting, File_Sighting


class FileSightingForm(ModelForm):
    class Meta:
        model = File_Sighting
        fields = ['file']

        labels = {
            'file': 'Insert images or videos',
        }

        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
                'multiple': True,
            })
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class SightingForm(ModelForm):
    class Meta:
        model = Sighting
        fields = ['Port', 'Date', 'Notes']

        labels = {
            'Port': 'Insert the port name',
            'Date': 'Insert the date of the sighting'
        }

        widgets = {
            'Port': forms.TextInput(attrs={'class': 'form-control form-control-lg secondary-text-color',
                                           'placeholder': 'Port name',
                                           'required': True,
                                           }),
            'Date': DateInput(attrs={'class': 'form-control form-control-lg secondary-text-color'}),
            'Notes': forms.Textarea(attrs={'class': 'form-control form-control-lg secondary-text-color',
                                           'placeholder': 'Notes',
                                           }),
        }

        help_texts = {
            'Date': ''
        }
