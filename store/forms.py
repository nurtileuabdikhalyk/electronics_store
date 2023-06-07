from django.contrib.auth.forms import UserCreationForm

from .models import *

from django import forms


class AddressForm(forms.ModelForm):
    def __init__(self, customer, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.customer = customer
        self.fields['customer'].initial = self.customer
        self.fields['order'] = forms.ModelChoiceField(
            queryset=Order.objects.filter(customer=self.customer), initial=True,
            widget=forms.Select(attrs={"class": "form-control", }, ))

    class Meta:
        model = Address
        fields = ('customer', 'order', 'phone', 'street', 'home_number', 'floor', 'door')
        widgets = {
            'customer': forms.Select(attrs={"class": "form-control", "readonly": "readonly"}),
            'phone': forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 708 484 57 67"}),
            'street': forms.TextInput(attrs={"class": "form-control"}),
            'home_number': forms.NumberInput(attrs={"class": "form-control"}),
            'floor': forms.NumberInput(attrs={"class": "form-control"}),
            'door': forms.NumberInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.ModelForm):
    login = forms.CharField(label='Логин',
                            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))

    class Meta:
        model = User
        fields = ('login', 'password',)


class CustomerForm(UserCreationForm):
    first_name = forms.CharField(label='Есіміңіз',
                                 widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Есіміңіз"}))
    last_name = forms.CharField(label='Тегіңіз',
                                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Тегіңіз"}))

    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))

    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
    password1 = forms.CharField(label='password1',
                                widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))
    password2 = forms.CharField(label='password2',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control", "placeholder": "Құпия сөзді қайталаңыз"}))

    phone = forms.CharField(label='Телефон',
                            widget=forms.TextInput(
                                attrs={"class": "form-control", "placeholder": "+7 708 484 57 67"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone')
