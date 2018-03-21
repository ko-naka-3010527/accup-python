from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as django_logout

login_url_def_name = 'accounts:login'

@login_required(login_url=login_url_def_name)
def login_redirect(request):
    return HttpResponseRedirect(
        reverse(
            'acclist:alllist',
            args=('html', request.user.username)))

def logout(request):
    django_logout(request)
    return HttpResponse(render(request, 'accounts/logout.html'))

def index(request):
    return login_redirect(request)
