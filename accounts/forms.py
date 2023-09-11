from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from .models import UserDetail, City, Country



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(),  max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True)


class CreateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm Password')

    class Meta:
        model = UserDetail
        fields = [ 'username', 'mail', 'mobile', 'name', 'country', 'nid', 'password' ]
        labels = {'mobile': 'Mobile NO', 'nid': 'National ID', 'mail': 'Email Address', 'name': 'Name' }
        widgets = {
            'password': forms.PasswordInput(),
        }


class UpdateMobileForm(forms.Form):
    mobile = forms.IntegerField(required=True, label='Mobile NO')

class UpdateMailForm(forms.Form):
    mail = forms.EmailField(required=True, label='Email Address')

class UpdateNameForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, label='Name')


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput, required=True,
                                       label='Current Password')
    new_password = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput, required=True,
                                   label='New Password')
    confirm_password = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput, required=True,
                                       label='Confirm Password')



