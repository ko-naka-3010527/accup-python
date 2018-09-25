from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.views import login as django_login
from django.contrib.auth.models import User as Djguser
from django.db.models import Q
from django.db import IntegrityError, transaction

from .permissions import is_users_url
from .renders import *
from .models import User as Accuser
from .models import Userlogin as Ulin
from .lib.form.signupform import *
from .lib.definitions.message import *
from .lib.definitions.message_error_update import *
from .lib.exception.accountsexception import AccountsException
from .lib.logic.update import update_accuser
from acclist.lib.logic.cryptoutil import encrypt_pass_cookie

import sys

login_url_def_name = 'accounts:login'

@login_required(login_url=login_url_def_name)
def login_redirect(request, fmt='html'):
    return HttpResponseRedirect(
        reverse(
            'acclist:alllist',
            args=(fmt, request.user.username)))

def login(request, fmt='html'):
    if "username" in request.POST and "password" in request.POST:
        un = request.POST["username"]
        pw = request.POST["password"]
        key = un
        val = encrypt_pass_cookie(pw)
        response = django_login(request, template_name='accounts/login.html')
        response.set_signed_cookie(key, val,
            salt=settings.COOKIE_SIGNED_SALT,
            max_age=settings.COOKIE_MAXAGE,
            secure=settings.COOKIE_SECURE,
            httponly=True)
        # insert login history
        ulin = Ulin()
        ulin.accup_user_id = get_object_or_404(
            Accuser, Q(accup_user_name=un))
        ulin.login_ip = request.META.get('REMOTE_ADDR')
        ulin.save()
    else:
        response = django_login(request, template_name='accounts/login.html')
    return response

def logout(request, fmt='html'):
    return django_logout(request, template_name='accounts/logout.html')

def index(request, fmt='html'):
    return login_redirect(request, fmt)

def update_view_main(request, fmt, username=None):
    # main process
    if fmt == 'html':
        if username is None:
            params = SignupForm(request.POST)
        else:
            params = UpdateForm(request.POST)
    else:
        raise Http404
    if not params.is_valid():
        if fmt == 'html':
            if username is None:
                result = UPDATE_RESPONSE['create_parameter_error']
            else:
                result = UPDATE_RESPONSE['update_parameter_error']
            return signup_form_render(
                request, username,
                newuser=(username is None),
                relay={'result': result},
                validate=params)
    if username is None:
        accuser = None
        djguser = None
    else:
        accuser = get_object_or_404(Accuser,
            Q(accup_user_name=username))
        djguser = get_object_or_404(Djguser,
            Q(username=username))
    # update
    result = None
    acc = None
    try:
        with transaction.atomic():
            acc = update_accuser(accuser, djguser, params)
        result = UPDATE_RESPONSE['ok']
    except IntegrityError as e:
        print(sys.exc_info())
        result = UPDATE_RESPONSE['transaction_error']
    except AccountsException as e:
        result = e.accounts_err_dict
    except Exception as e:
        result = UPDATE_RESPONSE['unexpected_error']
        print(sys.exc_info())
        # for test, raise it again
        raise e

    if fmt == 'html':
        # failure case
        if result['code'] != 0:
            return signup_form_render(
                request, username, newuser=(username is None),
                relay={'result': result})
        # success
        if username is None:
            return HttpResponseRedirect(
                reverse('accounts:create_success', kwargs={'fmt': fmt}))
        else:
            return HttpResponseRedirect(
                reverse('accounts:update_success',
                    kwargs={'fmt': fmt, 'username': username}))

@login_required(login_url=login_url_def_name)
def account_update_form(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    return HttpResponse(
        signup_form_render(request, username))

@login_required(login_url=login_url_def_name)
def account_update(request, fmt, username=None):
    # permission check
    is_users_url(request.user, username)

    # main view logic
    return update_view_main(request, fmt, username)

def account_create_form(request, fmt):
    return HttpResponse(
        signup_form_render(request, None, True))

def account_create(request, fmt):
    # main view logic
    return update_view_main(request, fmt, None)

def account_updatesuccess(request, username, fmt):
    # main process
    template = loader.get_template('accounts/updatesuccess.html')
    context = {
        'message': RESPONSE_MESSAGE['update_success'],
        'username': username,
    }
    return HttpResponse(template.render(context, request))

def account_createsuccess(request, fmt):
    # main process
    template = loader.get_template('accounts/createsuccess.html')
    context = {
        'message': RESPONSE_MESSAGE['create_success'],
    }
    return HttpResponse(template.render(context, request))

