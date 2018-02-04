from acclist.lib.definitions.specialconsts import *
from acclist.lib.definitions.message_error_update import *
from acclist.lib.exception.acclistexception import AcclistException
from acclist.models import *
import json

def is_new(param):
    return param == SELECT_OPTION['new']

def is_blank(param):
    return param == SELECT_OPTION['blank']

def udate_account(accup_user_id, account, form):
    # create new record of 'Account' if account is None
    if account is None:
        acc = Account()
    else:
        acc = account

    # account is alive or not
    acc.status = form.cleaned_data['status']

    # check if 'service' is another service name or not
    service_input = form.cleaned_data['service']
    if is_new(service_input):
        # register new service record
        newservice_input = form.cleaned_data['newservice']
        if newservice_input is None or newservice_input == "":
            raise AcclistException(
                UPDATE_RESPONSE['param_servicename'], "")
        service = Service()
        service.accup_user_id = accup_user_id
        service.service_name = newservice_input
        try:
            service.full_clean()
        except ValidationError as e:
            raise AcclistException(
                UPDATE_RESPONSE['param_servicename_validate'],
                py_e=json.dumps(e.message_dict))
        try:
            service.save()
            service.refresh_from_db()
        except DatabaseError:
            raise AcclistException(
                UPDATE_RESPONSE['db_service_save'])
        acc.service = service.id
    else:
        acc.service = service_input
    
    # TODO    

