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
from .lib.definitions.message_error_update import *
from .lib.definitions.specialconsts import *
#from .lib.logic.util import *
from .lib.exception.acclistexception import *
from .lib.form.update import *
from .lib.logic.update import *

import sys

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
    address_list = Address.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('address_text')
    phonenum_list = Phonenum.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('phonenum_text')
    service_list = Service.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('service_name')
    account_list = Account.objects.filter(
        accup_user_id_id__accup_user_name=username
    ).order_by('service__service_name')
    template = loader.get_template('acclist/accandmaillist.html')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'mail_list': mail_list,
        'address_list': address_list,
        'phonenum_list': phonenum_list,
        'service_list': service_list,
        'username': username,
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
        'username': username,
    }
    return HttpResponse(template.render(context, request))

def servicelinkedlist(request, username, serviceid, fmt):
    service_obj = get_object_or_404(Service,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=serviceid))
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(service=serviceid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': service_obj.service_name,
        'description': DESCRIPTION_MESSAGE['servicelinkedlist'],
    }
    return HttpResponse(template_acc.render(context_acc, request))

def maillinkedlist(request, username, mailid, fmt):
    mailaddr_obj = get_object_or_404(Mailaddr,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=mailid))
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(mailaddr1=mailid) | Q(mailaddr2=mailid) | Q(mailaddr3=mailid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': mailaddr_obj.mailaddr_text,
        'description': DESCRIPTION_MESSAGE['maillinkedlist'],
    }
    return HttpResponse(template_acc.render(context_acc, request))

def addresslinkedlist(request, username, addressid, fmt):
    address_obj = get_object_or_404(Address,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=addressid))
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(address=addressid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': address_obj.address_text,
        'description': DESCRIPTION_MESSAGE['addresslinkedlist'],
    }
    return HttpResponse(template_acc.render(context_acc, request))

def phonenumlinkedlist(request, username, phonenumid, fmt):
    phonenum_obj = get_object_or_404(Phonenum,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=phonenumid))
    account_list = Account.objects.filter(
        Q(accup_user_id_id__accup_user_name=username),
        Q(phonenum=phonenumid)
    ).order_by('service__service_name')
    template_acc = loader.get_template('acclist/acclist.html')
    context_acc = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': phonenum_obj.phonenum_text,
        'description': DESCRIPTION_MESSAGE['phonenumlinkedlist'],
    }
    return HttpResponse(template_acc.render(context_acc, request))

def updateform_lender(
    request, username, accid, fmt, newacc=False, relay=None, validate=None):
    if accid is None or newacc:
        account = Account()
    else:
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
        'newacc': newacc,
        'username': username,
    }
    return render(request, 'acclist/update.html', context)

def updateform(request, username, accid, fmt):
    return HttpResponse(
        updateform_lender(request, username, accid, fmt))

def insertform(request, username, fmt):
    return HttpResponse(
        updateform_lender(request, username, None, fmt, True))

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
            result = UPDATE_RESPONSE['update_parameter_error']
            return updateform_lender(
                request, username, accid, fmt, False,
                relay={'result': result},
                validate=params)
        # only html format request is allowed, at least for now..
        #elif fmt == 'json':
        #    HttpResponseBadRequest(json.dumps(params.errors))
    if accid is None:
        account = None
    else:
        account = get_object_or_404(Account,
            Q(accup_user_id_id__accup_user_name=username),
            Q(id=accid))
    user = get_object_or_404(User, Q(accup_user_name=username))
    # save updated information
    result = None
    acc = None
    try:
        with transaction.atomic():
            acc = udate_account(user.id, account, params, user)
        result = UPDATE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = UPDATE_RESPONSE['transaction_error']
    except AcclistException as e:
        result = e.acclist_err_dict
    except Exception as e:
        result = UPDATE_RESPONSE['unexpected_error']
        print(sys.exc_info())
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            if accid is None:
                return updateform_lender(
                    request, username, accid, fmt,
                    True, relay={'result': result})
            else:
                return updateform_lender(
                    request, username, accid, fmt,
                    False, relay={'result': result})
        if accid is None:
            return HttpResponseRedirect(
                reverse('acclist:accinsertsuccess', args=
                    (fmt, username, acc.id)))
        else:
            return HttpResponseRedirect(
                reverse('acclist:accupdatesuccess', args=
                    (fmt, username, accid)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

def insert(request, username, fmt):
    return update(request, username, None, fmt)

def updatesuccess(request, username, accid, fmt):
    template = loader.get_template('common/success.html')
    context = {
        'message': RESPONSE_MESSAGE['update_success'],
    }
    return accdetail(request, username, accid, fmt,
        template.render(context, request))

def insertsuccess(request, username, accid, fmt):
    template = loader.get_template('common/success.html')
    context = {
        'message': RESPONSE_MESSAGE['insert_success'],
    }
    return accdetail(request, username, accid, fmt,
        template.render(context, request))

