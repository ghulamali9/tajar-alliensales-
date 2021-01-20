from django import forms
from .models import Designation,Customers
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,Submit,Row,Column



class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ('designation',)
        labels = {
            'designation' : 'Designation'
        }


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ('customer_name','customer_email','customer_designation','customer_phone',
        'customer_address')         
        labels = {
            'customer_name' : 'Customer\'s Name',
            'customer_email' : 'Customer\'s Email',
            'customer_designation' : 'Customer\'s Designation',
            'customer_phone' : 'Customer\'s Phone No.',
            'customer_address' : 'Customer\'s Address'
        }

    def __init__(self,*args,**kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)
        self.fields['customer_designation'].empty_label = "Select Designation"
        self.fields['customer_designation'].queryset = Designation.objects.filter(is_deleted=False)
       

from django.contrib.auth import (
    authenticate
)
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input100'}))
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(f'User doesn\'t exist {username}')
            if not user.check_password(password):
                raise forms.ValidationError('Invalid Password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(UserLoginForm,self).clean(*args,**kwargs)

    
