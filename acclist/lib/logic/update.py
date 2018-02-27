from django.db.models import Q
from django.core.exceptions import ValidationError
from acclist.lib.definitions.specialconsts import *
from acclist.lib.definitions.message_error_update import *
from acclist.lib.exception.acclistexception import AcclistException
from acclist.models import *
import json

def is_new(param):
    return param == SELECT_OPTION['new']

def is_blank(param):
    return param == SELECT_OPTION['blank']

def mail_addr_prepare(mail_input, new_mail_input, num, accup_user_id, user):
    if is_blank(mail_input):
        return None
    elif is_new(mail_input):
        # register new mail address
        if (new_mail_input is None) or new_mail_input == "":
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['param_mailaddr' + str(num)])
            raise e
        mail = Mailaddr()
        mail.accup_user_id = user
        mail.mailaddr_text = new_mail_input
        try:
            mail.full_clean()
        except ValidationError as e:
            a_e = AcclistException()
            a_e.set_params(
                UPDATE_RESPONSE['param_mailaddr' + str(num) + '_validate'],
                py_e=json.dumps(e.message_dict))
            raise a_e
        try:
            mail.save()
            mail.refresh_from_db()
        except DatabaseError:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['db_mail' + str(num) + '_save'])
            raise e
        return mail
    else:
        try:
            mail_tmp = Mailaddr.objects.get(id=mail_input)
        except Mailaddr.DoesNotExist:
            mail_tmp = None
        if mail_tmp is None or mail_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_mail' + str(num) + '_mismatch'])
            raise e
        return mail_tmp

def udate_account(accup_user_id, account, form, user):
    # create new record of 'Account' if account is None
    if account is None:
        acc = Account()
        acc.accup_user_id = user
    else:
        acc = account
        if acc.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_account_mismatch'])
            raise e

    # account is alive or not
    acc.status = form.cleaned_data['status']

    # check if 'service' is new service name or not
    service_input = form.cleaned_data['service']
    if is_new(service_input):
        # register new service record
        newservice_input = form.cleaned_data['newservice']
        if newservice_input is None or newservice_input == "":
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['param_servicename'])
            raise e
        service = Service()
        service.accup_user_id = user
        service.service_name = newservice_input
        try:
            service.full_clean()
        except ValidationError as e:
            a_e = AcclistException()
            a_e.set_params(
                UPDATE_RESPONSE['param_servicename_validate'],
                py_e=json.dumps(e.message_dict))
            raise a_e
        try:
            service.save()
            service.refresh_from_db()
        except DatabaseError:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['db_service_save'])
            raise e
        acc.service = service
    else:
        try:
            service_tmp = Service.objects.get(id=service_input)
        except Service.DoesNotExist:
            service_tmp = None
        if service_tmp is None or service_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_service_mismatch'])
            raise e
        acc.service = service_tmp
    
    # Account ID
    acc.name = form.cleaned_data['accountid']

    # check if 'password' is updated or not
    if form.cleaned_data['updatepwd'] == 1:
        # updated
        if form.cleaned_data['password'] == form.cleaned_data['password_conf']:
            acc.passwd = form.cleaned_data['password']
        else:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['param_password_not_equal'])
            raise e

    # mailaddress
    mail1_input = form.cleaned_data['mailaddr1']
    mail2_input = form.cleaned_data['mailaddr2']
    mail3_input = form.cleaned_data['mailaddr3']
    new_mail1_input = form.cleaned_data['newmail1']
    new_mail2_input = form.cleaned_data['newmail2']
    new_mail3_input = form.cleaned_data['newmail3']
    print(new_mail1_input)
    print(new_mail2_input)
    print(new_mail3_input)
    if not is_blank(mail1_input) and not is_new(mail1_input):
        if not is_blank(mail2_input) and not is_new(mail2_input):
            if mail1_input == mail2_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
        if not is_blank(mail3_input) and not is_new(mail3_input):
            if mail1_input == mail3_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
    if not is_blank(mail2_input) and not is_new(mail2_input):
        if not is_blank(mail3_input) and not is_new(mail3_input):
            if mail2_input == mail3_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
    if not (new_mail1_input is None or new_mail1_input == ""):
        if not (new_mail2_input is None or new_mail2_input == ""):
            if new_mail1_input == new_mail2_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
        if not (new_mail3_input is None or new_mail3_input == ""):
            if new_mail1_input == new_mail3_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
    if not (new_mail2_input is None or new_mail2_input == ""):
        if not (new_mail3_input is None or new_mail3_input == ""):
            if new_mail2_input == new_mail3_input:
                e = AcclistException()
                e.set_params(
                    UPDATE_RESPONSE['param_mailaddr_duplicate'])
                raise e
    acc.mailaddr1 = mail_addr_prepare(
        mail1_input, new_mail1_input, 1, accup_user_id, user)
    acc.mailaddr2 = mail_addr_prepare(
        mail2_input, new_mail2_input, 2, accup_user_id, user)
    acc.mailaddr3 = mail_addr_prepare(
        mail3_input, new_mail3_input, 3, accup_user_id, user)

    # check if 'address' is new or blank or not
    address_input = form.cleaned_data['address']
    if is_blank(address_input):
        acc.address = None
    elif is_new(address_input):
        # register new address record
        newaddress_input = form.cleaned_data['newaddress']
        if newaddress_input is None or newaddress_input == "":
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['param_address'])
            raise e
        address = Address()
        address.accup_user_id = user
        address.address_text = newaddress_input
        try:
            address.full_clean()
        except ValidationError as e:
            a_e = AcclistException()
            a_e.set_params(
                UPDATE_RESPONSE['param_address_validate'],
                py_e=json.dumps(e.message_dict))
            raise a_e
        try:
            address.save()
            address.refresh_from_db()
        except DatabaseError:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['db_address_save'])
            raise e
        acc.address = address
    else:
        try:
            address_tmp = Address.objects.get(id=address_input)
        except Address.DoesNotExist:
            address_tmp = None
        if address_tmp is None or address_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_address_mismatch'])
            raise e
        acc.address = address_tmp

    # check if 'phonenum' is new or blank or not
    phonenum_input = form.cleaned_data['phonenum']
    if is_blank(phonenum_input):
        acc.phonenum = None
    elif is_new(phonenum_input):
        # register new phonenum record
        newphonenum_input = form.cleaned_data['newphonenum']
        if newphonenum_input is None or newphonenum_input == "":
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['param_phonenum'])
            raise e
        phonenum = Phonenum()
        phonenum.accup_user_id = user
        phonenum.phonenum_text = newphonenum_input
        try:
            phonenum.full_clean()
        except ValidationError as e:
            a_e = AcclistException()
            a_e.set_params(
                UPDATE_RESPONSE['param_phonenum_validate'],
                py_e=json.dumps(e.message_dict))
            raise a_e
        try:
            phonenum.save()
            phonenum.refresh_from_db()
        except DatabaseError:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['db_phonenum_save'])
            raise e
        acc.phonenum = phonenum
    else:
        try:
            phonenum_tmp = Phonenum.objects.get(id=phonenum_input)
        except Phonenum.DoesNotExist:
            phonenum_tmp = None
        if phonenum_tmp is None or phonenum_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_phonenum_mismatch'])
            raise e
        acc.phonenum = phonenum_tmp

    # check if 'link1' is blank or not
    link1_input = form.cleaned_data['link1']
    if is_blank(link1_input):
        acc.link1 = None
    else:
        try:
            acc_tmp = Account.objects.get(id=link1_input)
        except Account.DoesNotExist:
            acc_tmp = None
        if acc_tmp is None or acc_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_link1_mismatch'])
            raise e
        acc.link1 = acc_tmp

    # check if 'link2' is blank or not
    link2_input = form.cleaned_data['link2']
    if is_blank(link2_input):
        acc.link2 = None
    else:
        try:
            acc_tmp = Account.objects.get(id=link2_input)
        except Account.DoesNotExist:
            acc_tmp = None
        if acc_tmp is None or acc_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_link2_mismatch'])
            raise e
        acc.link2 = acc_tmp

    # check if 'link3' is blank or not
    link3_input = form.cleaned_data['link3']
    if is_blank(link3_input):
        acc.link3 = None
    else:
        try:
            acc_tmp = Account.objects.get(id=link3_input)
        except Account.DoesNotExist:
            acc_tmp = None
        if acc_tmp is None or acc_tmp.accup_user_id.id != accup_user_id:
            e = AcclistException()
            e.set_params(
                UPDATE_RESPONSE['user_link3_mismatch'])
            raise e
        acc.link3 = acc_tmp

    # multifactor type
    acc.multifactorauth_type = form.cleaned_data['multifactor_type']

    # multifactor info
    acc.multifactorauth_id = form.cleaned_data['multifactor_info']

    # secret Q&A
    acc.secret_q1 = form.cleaned_data['secq1']
    acc.secret_a1 = form.cleaned_data['seca1']
    acc.secret_q2 = form.cleaned_data['secq2']
    acc.secret_a2 = form.cleaned_data['seca2']
    acc.secret_q3 = form.cleaned_data['secq3']
    acc.secret_a3 = form.cleaned_data['seca3']

    # account register date
    acc.account_register_date = form.cleaned_data['register_date']

    # account unregister date
    acc.account_unregister_date = form.cleaned_data['unregister_date']

    # memo
    acc.memo = form.cleaned_data['memo']

    # save
    try:
        acc.full_clean()
    except ValidationError as e:
        msg_list = []
        for k, v in e.message_dict.items():
            msg_list.append(k + ": " + ",".join(v))
        a_e = AcclistException()
        a_e.set_params(
            UPDATE_RESPONSE['param_account_validate'],
            #py_e=json.dumps(e.message_dict, ensure_ascii=False))
            py_e=msg_list)
        raise a_e
    try:
        acc.save()
        acc.refresh_from_db()
    except DatabaseError:
        e = AcclistException()
        e.set_params(
            UPDATE_RESPONSE['db_account_save'])
        raise e
    return acc

