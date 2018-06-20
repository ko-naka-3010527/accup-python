from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import *
from .lib.definitions.message import *
from .lib.definitions.valuename import *
from .lib.definitions.common import *
from .lib.definitions.specialconsts import *
from .lib.logic.modelutil import *

def accdetail_render(
        request, username, account, relay, rendered=None):
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

def servicelinkedlist_render(
        request, service_obj, enc, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(service=service_obj.id))
    account_list = obj_sort_by_lambda(
        obj_list_decrypt(account_list, enc),
        lambda x:x.service.service_name)

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

def maillinkedlist_render(
        request, mailaddr_obj, enc, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(mailaddr1=mailaddr_obj.id) | Q(mailaddr2=mailaddr_obj.id) | Q(mailaddr3=mailaddr_obj.id))
    account_list = obj_sort_by_lambda(
        obj_list_decrypt(account_list, enc),
        lambda x:x.service.service_name)

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

def addresslinkedlist_render(
        request, address_obj, enc, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(address=address_obj.id))
    account_list = obj_sort_by_lambda(
        obj_list_decrypt(account_list, enc),
        lambda x:x.service.service_name)

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

def phonenumlinkedlist_render(
        request, phonenum_obj, enc, username, relay=None):
    account_list = Account.objects.filter(
        Q(accup_user_id__accup_user_name=username),
        Q(phonenum=phonenum_obj.id))
    account_list = obj_sort_by_lambda(
        obj_list_decrypt(account_list, enc),
        lambda x:x.service.service_name)

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
        request, username, accid, fmt, enc,
        newacc=False, relay=None, validate=None):
    if accid is None or newacc:
        account = Account()
    else:
        account = get_object_or_404(Account,
            Q(accup_user_id__accup_user_name=username),
            Q(id=accid))
        account.decrypt(enc)
    mail_list = Mailaddr.objects.filter(
        accup_user_id__accup_user_name=username)
    mail_list = obj_sort_by_property_name(
        obj_list_decrypt(mail_list, enc), 'mailaddr_text')
    service_list = Service.objects.filter(
        accup_user_id__accup_user_name=username)
    service_list = obj_sort_by_property_name(
        obj_list_decrypt(service_list, enc), 'service_name')
    addr_list = Address.objects.filter(
        accup_user_id__accup_user_name=username)
    addr_list = obj_sort_by_property_name(
        obj_list_decrypt(addr_list, enc), 'address_text')
    phone_list = Phonenum.objects.filter(
        accup_user_id__accup_user_name=username)
    phone_list = obj_sort_by_property_name(
        obj_list_decrypt(phone_list, enc), 'phonenum_text')
    account_list = Account.objects.filter(
        accup_user_id__accup_user_name=username).order_by('modifieddate')
    account_list = obj_list_decrypt(account_list, enc)
    context = {
        'title_text': 'Register new account' if newacc else 'Update account',
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

