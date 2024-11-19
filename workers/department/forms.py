from django import forms
from .models import  Worker

# Choices for Marital Status and Accommodation

class UserWorkerForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    department = forms.ChoiceField(  # Make sure to include the department field
        widget=forms.Select(attrs={'class': 'form-input'}),
        choices=[
            ('Ushering', 'Ushering'),
            ('Sanctuary', 'Sanctuary'),
            ('Spirit and Truth', 'Spirit and Truth'),
            ('Technical', 'Technical'),
            ('Light and Power', 'Light and Power'),
            ('Labour Room', 'Labour Room'),
            ('New Wine Media', 'New Wine Media'),
            ('Decoration', 'Decoration'),
            ('Welfare', 'Welfare'),
            ('Pastoral Care', 'Pastoral Care'),
        ]
    )

    class Meta:  # Correct indentation here
        model = Worker
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'department',
            'profile_picture',
        ]