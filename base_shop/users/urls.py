from django.urls import path
from .views import (
RegistUserView, HomeView, UserLoginView,
UserLogoutView,UserView,EditUserAndAddressView
)
from . import views

app_name = 'users'
urlpatterns = [
path('home/', HomeView.as_view(), name='home'),
path('regist/', RegistUserView.as_view(), name='regist'),
path('login/', UserLoginView.as_view(), name='user_login'),
path('logout/', UserLogoutView.as_view(), name='user_logout'),
path('user/', UserView.as_view(), name='user'),
path('edit/', views.EditUserAndAddressView.as_view(), name='edit')
]