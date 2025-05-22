from django.shortcuts import render, redirect
from django.views.generic import(
TemplateView, CreateView, FormView, View
)
from django.contrib.auth import authenticate, login, logout
from .forms import RegistForm, UserLoginForm
from django.urls import reverse_lazy

class HomeView(TemplateView):
  template_name = 'home.html'

class RegistUserView(CreateView):
  template_name = 'regist.html'
  form_class = RegistForm
  success_url = reverse_lazy('users:home')

class UserLoginView(FormView):
  template_name = 'user_login.html'
  form_class = UserLoginForm
  success_url = reverse_lazy('accounts:home')

class UserLogoutView(View):
  pass
