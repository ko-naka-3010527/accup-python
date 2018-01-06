from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.alllist, name='alllist'),
    path('accdetail/<str:username>/<int:accid>', views.accdetail, name='accdetail'),
]
