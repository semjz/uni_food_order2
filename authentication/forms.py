from django import forms
from .models import User


class SignUPForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields = {
            "username": self.fields["username"],
            "phone_number": self.fields["phone_number"],
            "password": self.fields["password"],
            "confirm_password": self.fields["confirm_password"],
        }

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if confirm_password != password:
            raise forms.ValidationError("Passwords must match!")

