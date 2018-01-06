from django.urls import path
from django.contrib.auth.views import login,logout
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', login,
        {'template_name': 'accounts/login.html'},
        name='login'),
    path('logout/', logout, name='logout'),
]

