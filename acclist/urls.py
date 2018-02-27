from django.urls import path

from . import views

app_name = 'acclist'
urlpatterns = [
    #path('', views.index, name='index'),
    path('<str:fmt>/<str:username>/', views.alllist, name='alllist'),
    path('<str:fmt>/<str:username>/account/<int:accid>/', views.accdetail, name='accdetail'),
    path('<str:fmt>/<str:username>/account/<int:accid>/updateform/', views.updateform, name='accupdateform'),
    path('<str:fmt>/<str:username>/account/new/', views.insertform, name='accinsertform'),
    path('<str:fmt>/<str:username>/account/<int:accid>/update/', views.update, name='accupdate'),
    path('<str:fmt>/<str:username>/account/new/insert/', views.insert, name='accinsert'),
    path('<str:fmt>/<str:username>/account/<int:accid>/update/success/', views.updatesuccess, name='accupdatesuccess'),
    path('<str:fmt>/<str:username>/account/<int:accid>/insert/success/', views.insertsuccess, name='accinsertsuccess'),
    path('<str:fmt>/<str:username>/mail/<int:mailid>/', views.maillinkedlist, name='maillinkedlist'),
    path('<str:fmt>/<str:username>/service/<int:serviceid>/', views.servicelinkedlist, name='servicelinkedlist'),
    path('<str:fmt>/<str:username>/address/<int:addressid>/', views.addresslinkedlist, name='addresslinkedlist'),
    path('<str:fmt>/<str:username>/phonenum/<int:phonenumid>/', views.phonenumlinkedlist, name='phonenumlinkedlist'),
]
