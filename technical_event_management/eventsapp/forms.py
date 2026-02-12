from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order, VendorProduct

class UserRegisterForm(UserCreationForm):
    membership = forms.ChoiceField(choices=CustomUser.MEMBERSHIP_CHOICES, initial='6m')

    class Meta:
        model = CustomUser
        fields = ('username','email','membership','password1','password2')

class VendorRegisterForm(UserCreationForm):
    vendor_category = forms.ChoiceField(choices=CustomUser.VENDOR_CATEGORY, widget=forms.RadioSelect)
    membership = forms.ChoiceField(choices=CustomUser.MEMBERSHIP_CHOICES, initial='6m')

    class Meta:
        model = CustomUser
        fields = ('username','email','vendor_category','membership','password1','password2')

class VendorProductForm(forms.ModelForm):
    class Meta:
        model = VendorProduct
        fields = ('name','quantity','price','image')

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pin_code = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES)