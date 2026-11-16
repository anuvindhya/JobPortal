from django import forms
from .models import Job


class Jobform(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'company_name',
            'description',
            'location',
            'salary'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'salary': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }