from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
  path('cart/', views.view_cart, name='view_cart'),
  path('add/<product_id>/', views.add_to_cart, name='add_to_cart'),
  path('remove/<item_id>/', views.remove_from_cart, name='remove_from_cart'),
  path('confirm/', views.order_confirm_view, name='confirm'),
  path('complete/', views.order_complete_view, name='order_complete'),
]