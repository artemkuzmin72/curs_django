from django import forms
from .models import Recipient, Message, Mailing
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 3})}

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["title", "start_time", "end_time", "status", "message", "recipients"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "message": forms.Select(attrs={"class": "form-select"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False  # неактивен до подтверждения email
        if commit:
            user.save()
        return user