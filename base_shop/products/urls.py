from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
  path('home/', views.HomeView.as_view(), name='home'),
  path('admin_login/', views.AdminLoginView.as_view(), name='admin_login')
]
