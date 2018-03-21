from django.urls import path
from django.contrib.auth.views import login as django_login
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', django_login,
        {'template_name': 'accounts/login.html'},
        name='login'),
    path('redirect/', views.login_redirect, name='loginredirect'),
    path('logout/', views.logout, name='logout'),
]

