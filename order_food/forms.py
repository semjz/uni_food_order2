from django import forms
from django.forms import modelformset_factory, formset_factory
from .models import Wallet

from .models import Food


class OrderForm(forms.Form):
    foods = forms.ModelChoiceField(queryset=Food.objects.all()
                                   , widget=forms.Select(attrs={'class': 'food-select'}),
                                   empty_label=None)
    quantity = forms.IntegerField(min_value=1
                                  , widget=forms.NumberInput(attrs={'class': 'quantity-input'}))


class ChargeWalletForm(forms.Form):
    amount = forms.IntegerField(min_value=100,
                                widget=forms.NumberInput(attrs={'class': 'charge-amount'}))


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = "__all__"

