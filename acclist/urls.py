from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.alllist, name='alllist'),
    path('<str:username>/accdetail/<int:accid>', views.accdetail, name='accdetail'),
]
