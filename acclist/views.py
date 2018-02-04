from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
# from django.views import generic
#from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError, transaction

from accounts.models import User
from .models import *
import json
from .lib.definitions.valuename import *
from .lib.definitions.message import *
from .lib.definitions.specialconsts import *
#from .lib.logic.util import *
from .lib.form.update import *
from .lib.logic.update import *

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

def accdetail(request, username, accid, fmt, relay=None):
    account = get_object_or_404(Account,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=accid))
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'title_text': 'Account detail',
        'account': account,
        'key_string': KEY_STRING,
        'relay': relay,
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

def updateform(request, username, accid, fmt, relay=None, validate=None):
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
        'key_string': KEY_STRING,
        'select_option': SELECT_OPTION,
        'relay': relay,
        'validate': validate,
    }
    return HttpResponse(template.render(context, request))

def update(request, username, accid, fmt):
    # validate params
    params = None
    if fmt == 'html':
        params = UpdateAccountForm(request.POST)
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    params = UpdateAccountForm(json.loads(request.body))
    else:
        raise Http404
    # main processing
    if not params.is_valid():
        # todo
        if fmt == 'html':
            return updateform(request, username, accid, fmt,
                relay=None, validate=params)
        # only html format request is allowed, at least for now..
        #elif fmt == 'json':
        #    HttpResponseBadRequest(json.dumps(params.errors))
    account = get_object_or_404(Account,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=accid))
    # todo
    try:
        with transaction.atomic():
            udate_account(account.accup_user_id, account, form)
    except IntegrityError as e:
        # handle exception
        raise "transaction failed"
    except AcclistException as e:
        # handle exception
        raise e

    # return response
    if fmt == 'html':
        return HttpResponseRedirect(
            reverse('acclist:accupdatesuccess', args=
                (fmt, username, accid,)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

def updatesuccess(request, username, accid, fmt):
    template = loader.get_template('common/success.html')
    context = {
        'message': RESPONSE_MESSAGE['success'],
    }
    return accdetail(request, username, accid, fmt,
        template.render(context, request))

