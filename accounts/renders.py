from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

from .models import User as Acclistuser

from .lib.definitions.valuename import *

def signup_form_render(
    request, userid, newuser=False, relay=None, validate=None):
    if not newuser:
        jguser = get_object_or_404(User, Q(username=userid))
        page_title = 'Update Acc-Up account'
    else:
        jguser = None
        page_title = 'Sign up Acc-Up account'
    context = {
        'title_text': page_title,
        'username': userid if not newuser else None,
        'email': jguser.email if not newuser else None,
        'newuser': newuser,
        'relay': relay,
        'validate': validate,
        'key_string': KEY_STRING,
    }
    return render(request, 'accounts/signup_form.html', context) 

