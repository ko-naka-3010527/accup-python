from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.views import login as django_login

from .permissions import is_users_url
from .renders import *

login_url_def_name = 'accounts:login'

@login_required(login_url=login_url_def_name)
def login_redirect(request, fmt='html'):
    return HttpResponseRedirect(
        reverse(
            'acclist:alllist',
            args=(fmt, request.user.username)))

def login(request, fmt='html'):
    return django_login(request, template_name='accounts/login.html')

def logout(request, fmt='html'):
    return django_logout(request, template_name='accounts/logout.html')
    #return HttpResponse(render(request, 'accounts/logout.html'))

def index(request, fmt='html'):
    return login_redirect(request, fmt)

def account_create_form(request, fmt):
    return HttpResponse(
        signup_form_render(request, None, True))

def account_create(request, fmt):
    return HttpResponse(render(request, 'accounts/logout.html'))

@login_required(login_url=login_url_def_name)
def account_update_form(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    return HttpResponse(
        signup_form_render(request, username))

@login_required(login_url=login_url_def_name)
def account_update(request, username, fmt):
    # permission check
    is_users_url(request.user, username)

    # main process
    return HttpResponse(render(request, 'accounts/logout.html'))

