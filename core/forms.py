from django import forms
from django.db import models
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','PayPal')
)
class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder':"1234 Main St"
    }))
    apartment_address = forms.CharField(required = False, widget = forms.TextInput(attrs={
        'placeholder':"Apartment or suite"
    }))
    country = CountryField(blank_label = '(select_country)').formfield(widget = CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id':'zip'
    }))
    zip = forms.CharField()
    same_biling_address = forms.BooleanField(required = False)
    payment_option = forms.ChoiceField(widget = forms.RadioSelect, choices = PAYMENT_CHOICES)
    save_info = forms.BooleanField(required = False)
    

