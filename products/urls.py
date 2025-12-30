from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView

app_name = 'products'

urlpatterns = [
  path('home/', views.HomeView.as_view(), name='home'),
  path('admin_login/', views.AdminLoginView.as_view(), name='admin_login'),
  path('list/', ProductListView.as_view(), name='product_list'),
  path('detail/<slug>', ProductDetailView.as_view(), name='product_detail')
]
