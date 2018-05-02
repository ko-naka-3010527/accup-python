from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:fmt>/', views.index, name='fmt'),
    path('html/login/', views.login, name='login'),
    path('html/redirect/', views.login_redirect, name='loginredirect'),
    path('html/logout/', views.logout, name='logout'),
    path('<str:fmt>/update/<str:username>/form/', views.account_update_form, name='update_form'),
    path('<str:fmt>/update/<str:username>/', views.account_update, name='update'),
    path('<str:fmt>/update/<str:username>/success/', views.account_updatesuccess, name='update_success'),
    path('<str:fmt>/create/form/', views.account_create_form, name='create_form'),
    path('<str:fmt>/create/', views.account_create, name='create'),
    path('<str:fmt>/create/success/', views.account_createsuccess, name='create_success'),
]

