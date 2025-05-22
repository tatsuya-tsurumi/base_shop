from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

class HomeView(TemplateView):
  template_name = 'items/home.html'

class AdminLoginView(View):
  def post(self, request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)

    if user is not None and user.is_staff:
      login(request, user)
      return redirect('/admin/')
    else:
      return render(request, 'items/home.html', {
        'error':"メールアドレスまたはパスワードが間違っています"
      })
  def get(self, request):
    return redirect('items:home')