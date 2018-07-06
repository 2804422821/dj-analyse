from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.account_login, name='account_login'),
    path('profile', views.account_profile, name='account_profile'),
    path('is_name_not_exists', views.account_username_not_exists, name='account_username_exists_valid'),
    path('is_email_not_exists', views.account_email_not_exists, name='account_email_not_exists_valid'),
    path('register', views.register, name='account_register'),
]
