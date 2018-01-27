from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
# from django.views import generic

from accounts.models import User
from .models import *

#class IndexView(generic.ListView):
#    template_name = 'acclist/index.html'
#    context_object_name = 'account_list'

#    def get_queryset(self):
#        return Account.objects.filter(
#            accup_user_id_id__accup_user_name=username
#        ).order_by('service__service_name')

#class DetailView(generic.DetailView):
#    model = Account
#    template_name = 'acclist/detail.html'

def index(request):
    return HttpResponse("Hello, world. You're at the 'acclist' index.")

def alllist(request, username, fmt):
    mail_list = Mailaddr.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('mailaddr_text')
    account_list = Account.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('service__service_name')
    template = loader.get_template('acclist/accandmaillist.html')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'mail_list': mail_list,
    }
    return HttpResponse(template.render(context, request))

def accdetail(request, username, accid, fmt):
    account = get_object_or_404(Account,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=accid))
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'title_text': 'Account detail',
        'account': account,
    }
    return HttpResponse(template.render(context, request))

def maillinkedlist(request, username, mailid, fmt):
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(mailaddr1=mailid) | Q(mailaddr2=mailid) | Q(mailaddr3=mailid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'title_text': 'Account list',
        'account_list': account_list,
    }
    return HttpResponse(template_acc.render(context_acc, request))

def updateform(request, username, accid, fmt):
    account = get_object_or_404(Account,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=accid))
    mail_list = Mailaddr.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('mailaddr_text')
    service_list = Service.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('service_name')
    addr_list = Address.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('address_text')
    phone_list = Phonenum.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('phonenum_text')
    account_list = Account.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('modifieddate')
    template = loader.get_template('acclist/update.html')
    context = {
        'title_text': 'Update account',
        'account': account,
        'mail_list': mail_list,
        'service_list': service_list,
        'addr_list': addr_list,
        'phone_list': phone_list,
        'account_list': account_list,
    }
    return HttpResponse(template.render(context, request))

#def update(request, username, accid):


