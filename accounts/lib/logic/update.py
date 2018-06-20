from django.db.utils import DatabaseError
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as Djguser
from accounts.lib.definitions.message_error_update import *
from accounts.lib.exception.accountsexception import AccountsException
from accounts.models import User as Accuser
from acclist.lib.logic.cryptoutil import CipherKey

import re

def is_valid_username(username):
    invalid_pattern = r"[^0-9A-Za-z_\-]"
    return re.search(invalid_pattern, username) is None

def update_accuser(accuser, djguser, form):
    # create new record of 'Accuser' if accuser is None
    if accuser is None and djguser is None:
        acc = Accuser()
    elif accuser is None or djguser is None:
        e = AccountsException()
        e.set_params(
            UPDATE_RESPONSE['unexpected_error'])
        raise e
    else:
        acc = accuser

    uname = ""
    pwd = ""
    email = ""
    cpwd = ""

    ## check params

    # username check
    if accuser is None:
        uname = form.cleaned_data['userid']
        if not is_valid_username(uname):
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_username_invalid'])
            raise e          
        tmp_acc = Accuser.objects.filter(accup_user_name=uname)
        tmp_djg = Djguser.objects.filter(username=uname)
        if tmp_acc.count() != 0 or tmp_djg.count() != 0:
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_username_already_exists'])
            raise e

    # password check
    updatepwd = False
    if accuser is None:
        updatepwd = True
    else:
        updatepwd = form.cleaned_data['updatepwd'] == 1
    if updatepwd:
        pwd = form.cleaned_data['password']
        pwd_cnf = form.cleaned_data['password_confirm']
        if pwd is None or pwd == "":
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_password'])
            raise e
        if pwd_cnf is None or pwd_cnf == "":
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_password_conf'])
            raise e
        if pwd != pwd_cnf:
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_password_not_equal'])
            raise e

    # email check
    updateemail = True
    email = form.cleaned_data['email']
    if accuser is not None:
        updateemail = not (email is None or email == "")

    # current password check
    if accuser is not None:
        cpwd = form.cleaned_data['current_password']
        if cpwd is None:
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_current_password_is_none'])
            raise e
        tmp_user = authenticate(
            username=djguser.username, password=cpwd)
        if tmp_user is None:
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['param_current_password_failure'])
            raise e

    ## save

    # djguser create/update
    try:
        if accuser is None:
            Djguser.objects.create_user(uname, email, pwd)
        else:
            if updatepwd:
                djguser.set_password(pwd)
            if updateemail:
                djguser.email = email
            djguser.save()
    except DatabaseError:
        e = AccountsException()
        e.set_params(
            UPDATE_RESPONSE['db_djgaccount_save'])
        raise e

    # accuser create/update
    accuser_update = False
    if accuser is None:
        acc.accup_user_name = uname
        ckey = CipherKey()
        ckey.generate(uname, pwd)
        acc.cipherkey = ckey.get_seed_base64_str()
        accuser_update = True
    elif updatepwd:
        ckey = CipherKey()
        ckey.load(acc, acc.accup_user_name, cpwd)
        ckey.update_seed(acc.accup_user_name, pwd)
        acc.cipherkey = ckey.get_seed_base64_str()
        accuser_update = True
    if accuser_update:
        try:
            acc.save()
            acc.refresh_from_db()
        except DatabaseError:
            e = AccountsException()
            e.set_params(
                UPDATE_RESPONSE['db_accaccount_save'])
            raise e

    return acc

