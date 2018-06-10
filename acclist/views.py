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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as django_logout
from django.core.signing import BadSignature, SignatureExpired

from accounts.models import User as Acclistuser
from accounts.permissions import is_users_url
from accounts.views import login_redirect
from accounts.views import logout as acc_logout
from .renders import *
from .models import *
import json
from .lib.definitions.common import *
from .lib.definitions.valuename import *
from .lib.definitions.message import *
from .lib.definitions.message_error_update import *
from .lib.definitions.specialconsts import *
#from .lib.logic.util import *
from .lib.exception.acclistexception import *
from .lib.exception.acccryptoexception import AcccryptoDecryptException
from .lib.form.update import *
from .lib.logic.update import *
from .lib.logic.cryptoutil import get_encryptor
from .lib.logic.modelutil import *

import sys


login_url_def_name = 'accounts:login'

#
# view functions
#

@login_required(login_url=login_url_def_name)
def index(request):
    return login_redirect(request)

def failure(request):
    return django_logout(request, template_name='acclist/failure.html')

@login_required(login_url=login_url_def_name)
def alllist(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # prepare lists (decryption and sort)
    mail_list = Mailaddr.objects.filter(
        accup_user_id__accup_user_name=username)
    mail_list = obj_sort_by_property_name(
        obj_list_decrypt(mail_list, enc), 'mailaddr_text')
    address_list = Address.objects.filter(
        accup_user_id__accup_user_name=username)
    address_list = obj_sort_by_property_name(
        obj_list_decrypt(address_list, enc), 'address_text')
    phonenum_list = Phonenum.objects.filter(
        accup_user_id__accup_user_name=username)
    phonenum_list = obj_sort_by_property_name(
        obj_list_decrypt(phonenum_list, enc), 'phonenum_text')
    service_list = Service.objects.filter(
        accup_user_id__accup_user_name=username)
    service_list = obj_sort_by_property_name(
        obj_list_decrypt(service_list, enc), 'service_name')
    account_list = Account.objects.filter(
        accup_user_id__accup_user_name=username)
    account_list = obj_sort_by_lambda(
        obj_list_decrypt(account_list, enc), lambda x:x.service.service_name)

    # set view arguments
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

@login_required(login_url=login_url_def_name)
def accdetail(request, username, accid, fmt, relay=None, rendered=None):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    account = get_object_or_404(Account,
        Q(accup_user_id__accup_user_name=username),
        Q(id=accid))

    return HttpResponse(
        accdetail_render(
            request, username, account.decrypt(enc), relay, rendered))

@login_required(login_url=login_url_def_name)
def servicelinkedlist(request, username, serviceid, fmt, relay=None):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    service_obj = get_object_or_404(Service,
        Q(accup_user_id__accup_user_name=username),
        Q(id=serviceid))

    return HttpResponse(servicelinkedlist_render(
        request, service_obj.decrypt(enc), enc, username, relay))

@login_required(login_url=login_url_def_name)
def servicedeleteconfirm(request, username, serviceid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # get account object
    service = get_object_or_404(Service,
        Q(accup_user_id__accup_user_name=username),
        Q(id=serviceid))
    # related accounts
    linked_tmp = Account.objects.filter(
        Q(service__id=service.id),
        Q(accup_user_id__accup_user_name=username))
    #decrypt
    service.decrypt(enc)
    related_account_list = obj_sort_by_lambda(
        obj_list_decrypt(linked_tmp, enc),
        lambda x:x.service.service_name)
    # delete information
    msg_template = loader.get_template('acclist/linkedinfodeleteconfirm.html')
    msg_context = {
        'info_id': service.id,
        'info_delete_url_key': 'acclist:servicedelete',
        'kind_of_info_text': KIND_OF_INFO_TEXT['service'],
        'target_info': service.service_name,
        'related_acounts': (None if len(related_account_list) == 0 else related_account_list),
        'username': username,
    }
    relay = msg_template.render(msg_context, request)
    # response
    template = loader.get_template('acclist/acclist.html')
    context = {
        'rendered': relay,
        'description': DESCRIPTION_MESSAGE['servicelinkedlist'],
        'key_value': service.service_name,
        'count': len(related_account_list),
        'account_list': related_account_list,
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def servicedelete(request, username, serviceid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    service = get_object_or_404(Service,
        Q(accup_user_id__accup_user_name=username),
        Q(id=serviceid))
    # delete account record
    result = None
    try:
        with transaction.atomic():
            service.delete()
        result = LINKED_INFO_DELETE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['transaction_error']
    except Exception as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['unexpected_error']
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            errmsg = loader.get_template('acclist/linkedinfoerrormsg.html')
            context = {
                'relay': result['message'],
            }
            return servicelinkedlist_render(
                request, service.decrypt(enc), enc, username,
                relay=errmsg.render(context, request))
        else:
            return HttpResponseRedirect(
                reverse('acclist:servicedeletesuccess', args=(fmt, username)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

@login_required(login_url=login_url_def_name)
def servicedeletesuccess(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('acclist/linkedinfodeletesuccess.html')
    context = {
        'title_text': 'Service has been deleted.',
        'message': RESPONSE_MESSAGE['service_delete_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def maillinkedlist(request, username, mailid, fmt, relay=None):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    mailaddr_obj = get_object_or_404(Mailaddr,
        Q(accup_user_id__accup_user_name=username),
        Q(id=mailid))
    return HttpResponse(maillinkedlist_render(
        request, mailaddr_obj.decrypt(enc), enc, username, relay))

@login_required(login_url=login_url_def_name)
def maildeleteconfirm(request, username, mailid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # get account object
    mailaddr = get_object_or_404(Mailaddr,
        Q(accup_user_id__accup_user_name=username),
        Q(id=mailid))
    # related accounts
    related_account_list = []
    linked_tmp = Account.objects.filter(
        Q(mailaddr1__id=mailaddr.id),
        Q(accup_user_id__accup_user_name=username))
    related_account_list.extend(linked_tmp)
    linked_tmp = Account.objects.filter(
        Q(mailaddr2__id=mailaddr.id),
        Q(accup_user_id__accup_user_name=username))
    related_account_list.extend(linked_tmp)
    linked_tmp = Account.objects.filter(
        Q(mailaddr3__id=mailaddr.id),
        Q(accup_user_id__accup_user_name=username))
    related_account_list.extend(linked_tmp)
    # decrypt
    mailaddr.decrypt(enc)
    related_account_list = obj_sort_by_lambda(
        obj_list_decrypt(related_account_list, enc),
        lambda x:x.service.service_name)

    # delete information
    msg_template = loader.get_template('acclist/linkedinfodeleteconfirm.html')
    msg_context = {
        'info_id': mailaddr.id,
        'info_delete_url_key': 'acclist:maildelete',
        'kind_of_info_text': KIND_OF_INFO_TEXT['mailaddr'],
        'target_info': mailaddr.mailaddr_text,
        'related_acounts': (None if len(related_account_list) == 0 else related_account_list),
        'username': username,
    }
    relay = msg_template.render(msg_context, request)
    # response
    template = loader.get_template('acclist/acclist.html')
    context = {
        'rendered': relay,
        'description': DESCRIPTION_MESSAGE['maillinkedlist'],
        'key_value': mailaddr.mailaddr_text,
        'count': len(related_account_list),
        'account_list': related_account_list,
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def maildelete(request, username, mailid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    mailaddr = get_object_or_404(Mailaddr,
        Q(accup_user_id__accup_user_name=username),
        Q(id=mailid))
    # delete account record
    result = None
    try:
        with transaction.atomic():
            mailaddr.delete()
        result = LINKED_INFO_DELETE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['transaction_error']
    except Exception as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['unexpected_error']
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            errmsg = loader.get_template('acclist/linkedinfoerrormsg.html')
            context = {
                'relay': result['message'],
            }
            return maillinkedlist_render(
                request, mailaddr.decrypt(enc), enc, username,
                relay=errmsg.render(context, request))
        else:
            return HttpResponseRedirect(
                reverse('acclist:maildeletesuccess', args=(fmt, username)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

@login_required(login_url=login_url_def_name)
def maildeletesuccess(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('acclist/linkedinfodeletesuccess.html')
    context = {
        'title_text': 'Mail address has been deleted.',
        'message': RESPONSE_MESSAGE['mail_delete_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def addresslinkedlist(request, username, addressid, fmt, relay=None):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    address_obj = get_object_or_404(Address,
        Q(accup_user_id__accup_user_name=username),
        Q(id=addressid))
    return HttpResponse(addresslinkedlist_render(
        request, address_obj.decrypt(enc), enc, username, relay))

@login_required(login_url=login_url_def_name)
def addressdeleteconfirm(request, username, addressid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # get account object
    address = get_object_or_404(Address,
        Q(accup_user_id__accup_user_name=username),
        Q(id=addressid))
    # related accounts
    related_account_list = []
    linked_tmp = Account.objects.filter(
        Q(address__id=address.id),
        Q(accup_user_id__accup_user_name=username)
    ).order_by('service__service_name')
    related_account_list.extend(linked_tmp)
    # decrypt
    address.decrypt(enc)
    related_account_list = obj_sort_by_lambda(
        obj_list_decrypt(related_account_list, enc),
        lambda x:x.service.service_name)
    # delete information
    msg_template = loader.get_template('acclist/linkedinfodeleteconfirm.html')
    msg_context = {
        'info_id': address.id,
        'info_delete_url_key': 'acclist:addressdelete',
        'kind_of_info_text': KIND_OF_INFO_TEXT['address'],
        'target_info': address.address_text,
        'related_acounts': (None if len(related_account_list) == 0 else related_account_list),
        'username': username,
    }
    relay = msg_template.render(msg_context, request)
    # response
    template = loader.get_template('acclist/acclist.html')
    context = {
        'rendered': relay,
        'description': DESCRIPTION_MESSAGE['addresslinkedlist'],
        'key_value': address.address_text,
        'count': len(related_account_list),
        'account_list': related_account_list,
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def addressdelete(request, username, addressid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    address = get_object_or_404(Address,
        Q(accup_user_id__accup_user_name=username),
        Q(id=addressid))
    # delete account record
    result = None
    try:
        with transaction.atomic():
            address.delete()
        result = LINKED_INFO_DELETE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['transaction_error']
    except Exception as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['unexpected_error']
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            errmsg = loader.get_template('acclist/linkedinfoerrormsg.html')
            context = {
                'relay': result['message'],
            }
            return addresslinkedlist_render(
                request, address.decrypt(enc), enc, username,
                relay=errmsg.render(context, request))
        else:
            return HttpResponseRedirect(
                reverse('acclist:addressdeletesuccess', args=(fmt, username)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

@login_required(login_url=login_url_def_name)
def addressdeletesuccess(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('acclist/linkedinfodeletesuccess.html')
    context = {
        'title_text': 'Address has been deleted.',
        'message': RESPONSE_MESSAGE['address_delete_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def phonenumlinkedlist(request, username, phonenumid, fmt, relay=None):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    phonenum_obj = get_object_or_404(Phonenum,
        Q(accup_user_id__accup_user_name=username),
        Q(id=phonenumid))
    return HttpResponse(phonenumlinkedlist_render(
        request, phonenum_obj.decrypt(enc), enc, username, relay))

@login_required(login_url=login_url_def_name)
def phonenumdeleteconfirm(request, username, phonenumid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # get account object
    phonenum = get_object_or_404(Phonenum,
        Q(accup_user_id__accup_user_name=username),
        Q(id=phonenumid))
    # related accounts
    related_account_list = []
    linked_tmp = Account.objects.filter(
        Q(phonenum__id=phonenum.id),
        Q(accup_user_id__accup_user_name=username)
    ).order_by('service__service_name')
    related_account_list.extend(linked_tmp)
    # decrypt
    phonenum.decrypt(enc)
    related_account_list = obj_sort_by_lambda(
        obj_list_decrypt(related_account_list, enc),
        lambda x:x.service.service_name)
    # delete information
    msg_template = loader.get_template('acclist/linkedinfodeleteconfirm.html')
    msg_context = {
        'info_id': phonenum.id,
        'info_delete_url_key': 'acclist:phonenumdelete',
        'kind_of_info_text': KIND_OF_INFO_TEXT['phonenum'],
        'target_info': phonenum.phonenum_text,
        'related_acounts': (None if len(related_account_list) == 0 else related_account_list),
        'username': username,
    }
    relay = msg_template.render(msg_context, request)
    # response
    template = loader.get_template('acclist/acclist.html')
    context = {
        'rendered': relay,
        'description': DESCRIPTION_MESSAGE['phonenumlinkedlist'],
        'key_value': phonenum.phonenum_text,
        'count': len(related_account_list),
        'account_list': related_account_list,
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def phonenumdelete(request, username, phonenumid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    phonenum = get_object_or_404(Phonenum,
        Q(accup_user_id_id__accup_user_name=username),
        Q(id=phonenumid))
    # delete account record
    result = None
    try:
        with transaction.atomic():
            phonenum.delete()
        result = LINKED_INFO_DELETE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['transaction_error']
    except Exception as e:
        print(sys.exc_info())
        result = LINKED_INFO_DELETE_RESPONSE['unexpected_error']
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            errmsg = loader.get_template('acclist/linkedinfoerrormsg.html')
            context = {
                'relay': result['message'],
            }
            return phonenumlinkedlist_render(
                request, phonenum.decrypt(enc), enc, username,
                relay=errmsg.render(context, request))
        else:
            return HttpResponseRedirect(
                reverse('acclist:phonenumdeletesuccess', args=(fmt, username)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

@login_required(login_url=login_url_def_name)
def phonenumdeletesuccess(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('acclist/linkedinfodeletesuccess.html')
    context = {
        'title_text': 'Phonenum has been deleted.',
        'message': RESPONSE_MESSAGE['phonenum_delete_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def updateform(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    return HttpResponse(
        updateform_render(request, username, accid, fmt, enc))

@login_required(login_url=login_url_def_name)
def insertform(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    return HttpResponse(
        updateform_render(request, username, None, fmt, enc, True))

@login_required(login_url=login_url_def_name)
def update(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
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
            return updateform_render(
                request, username, accid, fmt, enc, False,
                relay={'result': result},
                validate=params)
        # only html format request is allowed, at least for now..
        #elif fmt == 'json':
        #    HttpResponseBadRequest(json.dumps(params.errors))
    if accid is None:
        account = None
    else:
        account = get_object_or_404(Account,
            Q(accup_user_id__accup_user_name=username),
            Q(id=accid))
        account.decrypt(enc)
    # save updated information
    result = None
    acc = None
    try:
        with transaction.atomic():
            acc = update_account(user.id, account, params, user, enc)
        result = UPDATE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = UPDATE_RESPONSE['transaction_error']
    except AcclistException as e:
        print(sys.exc_info())
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
                return updateform_render(
                    request, username, accid, fmt, enc,
                    True, relay={'result': result})
            else:
                return updateform_render(
                    request, username, accid, fmt, enc,
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

@login_required(login_url=login_url_def_name)
def insert(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    return update(request, username, None, fmt)

@login_required(login_url=login_url_def_name)
def updatesuccess(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('common/success.html')
    context = {
        'message': RESPONSE_MESSAGE['update_success'],
    }
    return accdetail(request, username, accid, fmt,
        rendered=template.render(context, request))

@login_required(login_url=login_url_def_name)
def insertsuccess(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('common/success.html')
    context = {
        'message': RESPONSE_MESSAGE['insert_success'],
    }
    return accdetail(request, username, accid, fmt,
        rendered=template.render(context, request))

@login_required(login_url=login_url_def_name)
def deleteconfirm(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # get account object
    account = get_object_or_404(Account,
        Q(accup_user_id__accup_user_name=username),
        Q(id=accid))
    # related accounts
    related_account_list = []
    linked_tmp = Account.objects.filter(
        Q(link1__id=account.id),
        Q(accup_user_id__accup_user_name=username)
    ).order_by('service__service_name')
    related_account_list.extend(linked_tmp)
    linked_tmp = Account.objects.filter(
        Q(link2__id=account.id),
        Q(accup_user_id__accup_user_name=username)
    ).order_by('service__service_name')
    related_account_list.extend(linked_tmp)
    linked_tmp = Account.objects.filter(
        Q(link3__id=account.id),
        Q(accup_user_id__accup_user_name=username)
    ).order_by('service__service_name')
    related_account_list.extend(linked_tmp)
    # decrypt
    account.decrypt(enc)
    related_account_list = obj_sort_by_lambda(
        obj_list_decrypt(related_account_list, enc),
        lambda x:x.service.service_name)
    # delete information
    msg_template = loader.get_template('acclist/deleteconfirm.html')
    msg_context = {
        'service': account.service.service_name,
        'accname': account.name,
        'accid': accid,
        'username': username,
        'related_acounts': (related_account_list if len(related_account_list) > 0 else None),
    }
    relay = msg_template.render(msg_context, request)
    # response
    template = loader.get_template('acclist/accdetail.html')
    context = {
        'title_text': 'Delete account',
        'account': account,
        'key_string': KEY_STRING,
        'rendered': relay,
        'username': username,
        'delete': True,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url=login_url_def_name)
def delete(request, username, accid, fmt):
    # permission check
    is_users_url(request.user, username)

    # prepare decryption
    user = get_object_or_404(Acclistuser, Q(accup_user_name=username))
    try:
        enc = get_encryptor(request, user)
    except (KeyError, BadSignature, SignatureExpired):
        return failure(request)
    except AcccryptoDecryptException as e:
        #return failure(request)
        raise e

    # main process
    # validate params
    params = None
    account = get_object_or_404(Account,
        Q(accup_user_id__accup_user_name=username),
        Q(id=accid))
    # delete account record
    result = None
    acc = None
    try:
        with transaction.atomic():
            account.delete()
        result = DELETE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = DELETE_RESPONSE['transaction_error']
    except Exception as e:
        result = DELETE_RESPONSE['unexpected_error']
        print(sys.exc_info())
        # for test, raise it again
        raise e

    # return response
    if fmt == 'html':
        if result['code'] != 0:
            return accdetail_render(request, username, account.decrypt(enc),
                relay={'result': result})
        else:
            return HttpResponseRedirect(
                reverse('acclist:accdeletesuccess', args=(fmt, username)))
    # only html format request is allowed, at least for now..
    #elif fmt == 'json':
    #    return HttpResponseRedirect(
    #        reverse('acclist:accdetail', args=
    #            (fmt, username, accid,)))

@login_required(login_url=login_url_def_name)
def deletesuccess(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    template = loader.get_template('acclist/deletesuccess.html')
    context = {
        'title_text': 'Account has been deleted.',
        'message': RESPONSE_MESSAGE['delete_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

