from django.shortcuts import render, redirect
from django.views.generic import(
TemplateView, CreateView, FormView, View
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib import messages

class HomeView(TemplateView):
  template_name = 'home.html'

class RegistUserView(CreateView):
  template_name = 'regist.html'
  form_class = RegistForm
  success_url = reverse_lazy('users:home')

class UserLoginView(FormView):
  template_name = 'user_login.html'
  form_class = UserLoginForm
  success_url = reverse_lazy('users:user')

  def form_valid(self, form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = authenticate(email=email, password=password)
    if user:
      login(self.request, user)
      return super().form_valid(form)
    else:
      messages.error(self.request, 'メールアドレスまたはパスワードが間違っています')
      return self.form_invalid(form)
    

class UserLogoutView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'user_logout.html')
  def post(self, request, *args, **kwargs):
    logout(request)
    return redirect('users:home')
  
class UserView(LoginRequiredMixin, TemplateView):
  template_name = 'user.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user'] = self.request.user
    return context

