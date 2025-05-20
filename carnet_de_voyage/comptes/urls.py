from django.urls import path
from .views import register_view, login_view, register, login

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('register-client/', register, name='register-client'),
    path('login-client/', login, name='login-client'),
]
