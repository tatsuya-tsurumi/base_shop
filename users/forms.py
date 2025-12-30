from django import forms
from .models import User,Address
from django.contrib.auth.password_validation import validate_password
from .utils import get_country_list, PREFECTURES

class RegistForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    widgets = {
    'password': forms.PasswordInput(),
    }
    labels = {
    'username': 'お名前(フルーネーム)',
    'email': 'メールアドレス',
    'password': 'パスワード',
    }

  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data['password'], user)
    user.set_password(self.cleaned_data['password'])
    user.save()
    return user
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.label_suffix = ''

class UserLoginForm(forms.Form):
  email = forms.EmailField(label='メールアドレス', label_suffix='')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), label_suffix='')
  
class AddressForm(forms.ModelForm):
  country = forms.ChoiceField(
    choices = [(country, country) for country in get_country_list()],
    label='国名',
    widget=forms.Select(attrs={
      'class': 'form-select'
    })
  )
  prefecture = forms.ChoiceField(
    choices=[(pref, pref) for pref in PREFECTURES],
    label='都道府県',
    widget=forms.Select(attrs={
      'class': 'form-select'
    })
  )
  class Meta:
    model = Address
    fields = ['postal_code', 'country', 'prefecture', 'city', 'street']
    labels = {
      'postal_code': '郵便番号',
      'country': '国名',
      'prefecture': '都道府県',
      'city': '市区町村',
      'street': '丁目以下',
    }
    widgets = {
      'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
      'city': forms.TextInput(attrs={'class': 'form-control'}),
      'street': forms.TextInput(attrs={'class': 'form-control'}),
    }
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.label_suffix = ''
    