from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import Student, Book

class IssueBookForm(forms.Form):
    name2 = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Select Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    isbn2 = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        label="Select Book",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
