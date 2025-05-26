from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegistForm(forms.ModelForm):

  class Meta:
    model = User
    fields = ['username', 'email', 'address', 'password']
    widgets = {
    'password': forms.PasswordInput(),
    }
    labels = {
    'username': '名前',
    'email': 'メールアドレス',
    'address': '住所',
    'password': 'パスワード',
    }

  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data['password'], user)
    user.set_password(self.cleaned_data['password'])
    user.save()
    return user

class UserLoginForm(forms.Form):
  email = forms.EmailField(label='メールアドレス', label_suffix='')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), label_suffix='')