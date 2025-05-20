from django.urls import path
from .views import register_view, login_view
from .views import register

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('register-client/', register, name='register-client'),
]
