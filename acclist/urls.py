from django.urls import path

from . import views

app_name = 'acclist'
urlpatterns = [
    #path('', views.index, name='index'),

    # account list
    path('<str:fmt>/<str:username>/', views.alllist, name='alllist'),
    path('<str:fmt>/<str:username>/mail/<int:mailid>/', views.maillinkedlist, name='maillinkedlist'),
    path('<str:fmt>/<str:username>/service/<int:serviceid>/', views.servicelinkedlist, name='servicelinkedlist'),
    path('<str:fmt>/<str:username>/address/<int:addressid>/', views.addresslinkedlist, name='addresslinkedlist'),
    path('<str:fmt>/<str:username>/phonenum/<int:phonenumid>/', views.phonenumlinkedlist, name='phonenumlinkedlist'),

    # actions against account linked informations
    path('<str:fmt>/<str:username>/mail/<int:mailid>/deleteform/', views.maildeleteconfirm, name='maildeleteconfirm'),
    path('<str:fmt>/<str:username>/mail/<int:mailid>/delete/', views.maildelete, name='maildelete'),
    path('<str:fmt>/<str:username>/mail/none/deletesuccess/', views.maildeletesuccess, name='maildeletesuccess'),
    path('<str:fmt>/<str:username>/service/<int:serviceid>/deleteform/', views.servicedeleteconfirm, name='servicedeleteconfirm'),
    path('<str:fmt>/<str:username>/service/<int:serviceid>/delete/', views.servicedelete, name='servicedelete'),
    path('<str:fmt>/<str:username>/service/none/deletesuccess/', views.servicedeletesuccess, name='servicedeletesuccess'),
    path('<str:fmt>/<str:username>/address/<int:addressid>/deleteform/', views.addressdeleteconfirm, name='addressdeleteconfirm'),
    path('<str:fmt>/<str:username>/address/<int:addressid>/delete/', views.addressdelete, name='addressdelete'),
    path('<str:fmt>/<str:username>/address/none/deletesuccess/', views.addressdeletesuccess, name='addressdeletesuccess'),
    path('<str:fmt>/<str:username>/phonenum/<int:phonenumid>/deleteform/', views.phonenumdeleteconfirm, name='phonenumdeleteconfirm'),
    path('<str:fmt>/<str:username>/phonenum/<int:phonenumid>/delete/', views.phonenumdelete, name='phonenumdelete'),
    path('<str:fmt>/<str:username>/phonenum/none/deletesuccess/', views.phonenumdeletesuccess, name='phonenumdeletesuccess'),
 
    # account detail
    path('<str:fmt>/<str:username>/account/<int:accid>/', views.accdetail, name='accdetail'),

    # account update
    path('<str:fmt>/<str:username>/account/<int:accid>/updateform/', views.updateform, name='accupdateform'),
    path('<str:fmt>/<str:username>/account/<int:accid>/update/', views.update, name='accupdate'),
    path('<str:fmt>/<str:username>/account/<int:accid>/updatesuccess/', views.updatesuccess, name='accupdatesuccess'),

    # account insert
    path('<str:fmt>/<str:username>/account/new/', views.insertform, name='accinsertform'),
    path('<str:fmt>/<str:username>/account/new/insert/', views.insert, name='accinsert'),
    path('<str:fmt>/<str:username>/account/<int:accid>/insertsuccess/', views.insertsuccess, name='accinsertsuccess'),

    # accountdelete
    path('<str:fmt>/<str:username>/account/<int:accid>/deleteform/', views.deleteconfirm, name='accdeleteconfirm'),
    path('<str:fmt>/<str:username>/account/<int:accid>/delete/', views.delete, name='accdelete'),
    path('<str:fmt>/<str:username>/account/none/deletesuccess/', views.deletesuccess, name='accdeletesuccess'),
]
