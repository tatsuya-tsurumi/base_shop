from django.shortcuts import render, redirect
from django.views.generic import(
TemplateView, CreateView, FormView, View,UpdateView
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from orders.models import Order

User = get_user_model()

class HomeView(TemplateView):
  template_name = 'users/home.html'

class RegistUserView(CreateView):
  template_name = 'users/regist.html'
  form_class = RegistForm
  success_url = reverse_lazy('users:home')

class UserLoginView(FormView):
  template_name = 'users/user_login.html'
  form_class = UserLoginForm
  success_url = reverse_lazy('users:home')

  def form_valid(self, form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = authenticate(email=email, password=password)
    if user:
      login(self.request, user)
      messages.success(self.request, f'おかえりなさい、{user.username}さん')
      return super().form_valid(form)
    else:
      messages.error(self.request, 'メールアドレスまたはパスワードが間違っています')
      return self.form_invalid(form)
    

class UserLogoutView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'users/user_logout.html')
  def post(self, request, *args, **kwargs):
    logout(request)
    return redirect('users:home')
  

class UserView(LoginRequiredMixin, TemplateView):
  template_name = 'users/user.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    orders = Order.objects.filter(user=self.request.user).order_by('-created_at')

    for order in orders:  
      order.items_with_total = []
      for item in order.items.all():
        item.total_price = item.product.price * item.quantity
        order.items_with_total.append(item)
    context['orders'] = orders
    return context

class EditUserView(LoginRequiredMixin, UpdateView):
  model = User
  template_name = 'users/edit.html'
  fields = ['username', 'email', 'address']
  success_url = reverse_lazy('users:user')

  def get_object(self):
    return self.request.user