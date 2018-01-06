from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
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
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'account_list': account_list,
    }
    template_mail = loader.get_template('acclist/maillist.html')
    context_mail = {
        'mail_list': mail_list,
    }
    return HttpResponse(
        template_mail.render(context_mail, request) +
        template_acc.render(context_acc, request))

def accdetail(request, username, accid):
    try:
        account = Account.objects.get(
            Q(accup_user_id_id__accup_user_name=username),
            Q(id=accid)
        )
    except Account.DoesNotExist:
        raise Http404("Requested account information does not exist")
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'account': account
    }
    return HttpResponse(template.render(context, request))

def maillinkedlist(request, username, mailid):
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(mailaddr1=mailid) | Q(mailaddr2=mailid) | Q(mailaddr3=mailid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'account_list': account_list,
    }
    return HttpResponse(template_acc.render(context_acc, request))

