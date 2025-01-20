from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Request, Query

class CompanyRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        return user

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['item', 'quantity']

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['issue', 'image']
