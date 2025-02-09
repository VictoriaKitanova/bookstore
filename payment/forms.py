"""
This module contains the form definitions used for handling shipping and payment details.
"""
from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    """
    Form for capturing shipping address information from the user.
    """
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Full name'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Address'}), required=True)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        """
         Metadata for the ShippingForm.

        - Defines the model (ShippingAddress) to which the form is related.
        - Specifies the fields to be included in the form
        - Excludes the user field to avoid collecting user information directly from the form.
        """
        model = ShippingAddress
        fields = ('shipping_full_name',
                  'shipping_email',
                  'shipping_address1',
                  'shipping_city',
                  'shipping_country'
                )

        exclude = ['user', ]

class PaymentForm(forms.Form):
    """
    Form for capturing payment information from the user.
    """
    card_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Name on card'}), required=True)
    card_number = forms.IntegerField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Card number'}), required=True)
    card_exp_date = forms.DateTimeField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Expiration date'}), required=True)
    card_cvv_number = forms.IntegerField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'CVV code'}), required=True)
    card_address = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Billing address'}), required=True)
    card_city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Billing city'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Billing country'}), required=True)
