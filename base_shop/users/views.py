from django.shortcuts import render, redirect
from django.views.generic import(
TemplateView, CreateView, FormView, View,UpdateView
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django import forms
from orders.models import Order
from .models import Address
from .forms import UserLoginForm
import pycountry

User = get_user_model()

PREFECTURES = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "岐阜県", "静岡県", "愛知県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "秋田県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

def get_country_list():
  return [country.name for country in pycountry.countries]

class RegistUserView(View):
  def get(self, request, *args, **kwargs):
    countries = get_country_list()
    return render(request, 'users/regist.html', {
      "countries": countries,
      "prefectures": PREFECTURES
    })
  
  def post(self, request, *args, **kwargs):
    # ユーザー情報の取得
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # 住所情報の取得
    postal_code = request.POST.get('postal_code') or ""
    country = request.POST.get('country') or ""
    prefecture = request.POST.get('prefecture') or ""
    city = request.POST.get('city') or ""
    street = request.POST.get('street') or ""

    # 名前・メールアドレス・パスワードどれかがなかった場合の処理
    if not username or not email or not password:
      messages.error(request, "名前・メールアドレス・パスワード全て必須です")
      return render(request, 'users/regist.html')
    
    # メールアドレスが重複したいた場合の処理
    if User.objects.filter(email=email).exists():
      messages.error(request, "このメールアドレスは既に登録されています")
      return render(request, 'users/regist.html')
    
    #ユーザー情報の登録処理
    user = User.objects.create(
      username=username,
      email=email
    )
    user.set_password(password)
    user.save()

    #住所情報の登録処理
    Address.objects.create(
      user=user,
      postal_code=postal_code,
      country=country,
      prefecture=prefecture,
      city=city,
      street=street
    )

    login(request, user)
    messages.success(request, f"{username}さんの登録が完了しました")
    return redirect('users:home')



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

    try:
      address = Address.objects.get(user=self.request.user)
      address_str = f"{address.prefecture}{address.city}{address.street}"
    except Address.DoesNotExist:
      address_str = "住所未登録"

    context['address_str'] = address_str
    return context
  
class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    fields = ['postal_code', 'country', 'prefecture', 'city', 'street']

class EditUserAndAddressView(LoginRequiredMixin, View):
  def get(self, request):
    countries = get_country_list()
    user_form = UserForm(instance=request.user)
    address, created = Address.objects.get_or_create(user=request.user)
    address_form = AddressForm(instance=address)
    return render(request, 'users/edit.html', {
      'user_form': user_form,
      'address_form': address_form,
      "countries": countries,
      "prefectures": PREFECTURES
    })

  def post(self, request):
    user_form = UserForm(request.POST, instance=request.user)
    address, _ = Address.objects.get_or_create(user=request.user)
    address_form = AddressForm(request.POST, instance=address)

    if user_form.is_valid() and address_form.is_valid():
      user_form.save()
      address_form.save()
      messages.success(request, 'ユーザー情報を更新しました')
      return redirect('users:user')
    
    return render(request, 'users/edit.html', {
      'user_form': user_form,
      'address_form': address_form
    })