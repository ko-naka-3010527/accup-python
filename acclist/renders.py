from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import *
from .lib.definitions.message import *
from .lib.definitions.valuename import *
from .lib.definitions.common import *
from .lib.definitions.specialconsts import *

def accdetail_render(request, username, account, relay, rendered=None):
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'title_text': 'Account detail',
        'account': account,
        'key_string': KEY_STRING,
        'relay': relay,
        'rendered': rendered,
        'username': username,
    }
    return template.render(context, request)

def servicelinkedlist_render(request, service_obj, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(service=service_obj.id)
    ).order_by('service__service_name')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': service_obj.service_name,
        'description': DESCRIPTION_MESSAGE['servicelinkedlist'],
        'rendered': relay,
    }
    return render(request, 'acclist/acclist.html', context)

def maillinkedlist_render(request, mailaddr_obj, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(mailaddr1=mailaddr_obj.id) | Q(mailaddr2=mailaddr_obj.id) | Q(mailaddr3=mailaddr_obj.id)
    ).order_by('service__service_name')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': mailaddr_obj.mailaddr_text,
        'description': DESCRIPTION_MESSAGE['maillinkedlist'],
        'rendered': relay,
    }
    return render(request, 'acclist/acclist.html', context)

def addresslinkedlist_render(request, address_obj, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(address=address_obj.id)
    ).order_by('service__service_name')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': address_obj.address_text,
        'description': DESCRIPTION_MESSAGE['addresslinkedlist'],
        'rendered': relay,
    }
    return render(request, 'acclist/acclist.html', context)

def phonenumlinkedlist_render(request, phonenum_obj, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(phonenum=phonenum_obj.id)
    ).order_by('service__service_name')
    context = {
        'title_text': 'Account list',
        'account_list': account_list,
        'count': len(account_list),
        'username': username,
        'key_value': phonenum_obj.phonenum_text,
        'description': DESCRIPTION_MESSAGE['phonenumlinkedlist'],
        'rendered': relay,
    }
    return render(request, 'acclist/acclist.html', context)

def updateform_render(
    request, username, accid, fmt, newacc=False, relay=None, validate=None):
    if accid is None or newacc:
        account = Account()
    else:
        account = get_object_or_404(Account,
            Q(accup_user_id__accup_user_name=username),
            Q(id=accid))
    mail_list = Mailaddr.objects.filter(
        accup_user_id__accup_user_name=username
    ).order_by('mailaddr_text')
    service_list = Service.objects.filter(
        accup_user_id__accup_user_name=username
    ).order_by('service_name')
    addr_list = Address.objects.filter(
        accup_user_id__accup_user_name=username
    ).order_by('address_text')
    phone_list = Phonenum.objects.filter(
        accup_user_id__accup_user_name=username
    ).order_by('phonenum_text')
    account_list = Account.objects.filter(
        accup_user_id__accup_user_name=username
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
        'other_string': OTHER_STRING,
        'common_string': COMMON_STRING,
        'select_option': SELECT_OPTION,
        'relay': relay,
        'validate': validate,
        'newacc': newacc,
        'username': username,
    }
    return render(request, 'acclist/update.html', context)

