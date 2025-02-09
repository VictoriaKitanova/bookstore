"""
This module contains the forms for user creation, updating user information,
and handling user profile details in the accounts app.
"""
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile

class UserInfoForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form is used to update the user's personal profile information 
    such as phone number, address, city, and country.
    """
    phone = forms.IntegerField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
    address = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Address'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

    class Meta:
        """
        Meta class for defining the model and fields used in the form.

        This class is used to specify which fields 
        should be included in the form.
        """
        model = Profile
        fields = ('phone', 'address', 'city', 'country', )


class UpdateUserForm(UserChangeForm):
    """
    Form for updating existing user details.

    This form allows the user to update their username, first name, last name,
    and email address while hiding the password fields.
    """
    # Hide password stuff
    password = None
    # Get other fields
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

    class Meta:
        """
        Meta class for defining the model and fields used in the form.

        This class is used to specify which fields 
        should be included in the form.
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.</small></span>'
        )

class SignUpForm(UserCreationForm):
    """
    Form for user registration.

    This form allows a new user to sign up by providing their username, first name,
    last name, email, and password. It also includes password validation and confirmation.
    """
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        """
        Meta class for defining the model and fields used in the form.

        This class is used to specify which fields 
        should be included in the form.
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted"><small>Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.</small></span>'
        )

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password can\'t be too similar to your other personal information.</li>'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password can\'t be a commonly used password.</li>'
            '<li>Your password can\'t be entirely numeric.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text =  (
            '<span class="form-text text-muted">'
            '<small>Enter the same password as before, for verification.</small>'
            '</span>'
        )
