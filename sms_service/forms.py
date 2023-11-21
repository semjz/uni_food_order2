from django import forms


class SendSMSForm(forms.Form):
    phone_number = forms.CharField(max_length=13, min_length=11)
    message = forms.CharField(max_length=100)
