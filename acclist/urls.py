from django.urls import path

from . import views

app_name = 'acclist'
urlpatterns = [
    #path('', views.index, name='index'),
    path('<str:fmt>/<str:username>/', views.alllist, name='alllist'),
    path('<str:fmt>/<str:username>/account/<int:accid>/', views.accdetail, name='accdetail'),
    path('<str:fmt>/<str:username>/account/<int:accid>/updateform/', views.updateform, name='accupdateform'),
    path('<str:fmt>/<str:username>/account/<int:accid>/update/', views.updateform, name='accupdate'),
    path('<str:fmt>/<str:username>/mail/<int:mailid>/', views.maillinkedlist, name='maillinkedlist'),
]
