from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.db.models import Q

from accounts.models import User
from .models import Account, Mailaddr

def index(request):
    return HttpResponse("Hello, world. You're at the 'acclist' index.")

def alllist(request, username):
    mail_list = Mailaddr.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('mailaddr_text')
    account_list = Account.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('service__service_name')
    template = loader.get_template('acclist/alllist.html')
    context = {
        'account_list': account_list,
        'mail_list': mail_list,
    }
    return HttpResponse(template.render(context, request))

def accdetail(request, username, accid):
    account = Account.objects.get(
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=accid)
    )
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'account': account
    }
    return HttpResponse(template.render(context, request))

