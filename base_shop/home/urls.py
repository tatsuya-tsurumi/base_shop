from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  
    path('error-test/', views.trigger_error, name='error_test'),
]