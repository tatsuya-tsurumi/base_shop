from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import Product


class HomeView(TemplateView):
  template_name = 'products/home.html'
  

class AdminLoginView(View):
  def post(self, request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)

    if user is not None and user.is_staff:
      login(request, user)
      return redirect('/admin/')
    else:
      return render(request, 'products/home.html', {
        'error':"メールアドレスまたはパスワードが間違っています"
      })
  def get(self, request):
    return redirect('products:home')

class ProductListView(ListView):
  model = Product
  template_name = 'products/product_list.html'
  context_object_name = 'products'