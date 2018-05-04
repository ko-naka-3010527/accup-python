def obj_sort_by(obj_list, prop_name):
    new_obj_list = obj_list.copy()
    new_obj_list.sort(key=lambda x:getattr(x, prop_name))
    return new_obj_list

def obj_sort_by_proc(obj_list, proc):
    new_obj_list = obj_list.copy()
    new_obj_list.sort(key=proc)
    return new_obj_list

def obj_decrypt(obj, prop_name, enc):
    cpy_obj = obj.copy()
    setattr(cpy_obj, prop_name, enc.decrypt(getattr(obj, prop_name)))
    return cpy_obj

def obj_list_decrypt(obj_list, prop_name, enc):
    new_obj_list = []
    for obj in obj_list:
        new_obj_list.append(obj_decrypt(obj, prop_name, enc))
    return new_obj_list

def sort_and_decrypt_account_list(acclist, enc, sort_proc=None):
    alist = obj_list_decrypt(acclist, 'name', enc)
    alist = obj_list_decrypt(alist, 'passwd', enc)
    alist = obj_list_decrypt(alist, 'multifactorauth_type', enc)
    alist = obj_list_decrypt(alist, 'multifactorauth_id', enc)
    alist = obj_list_decrypt(alist, 'secret_q1', enc)
    alist = obj_list_decrypt(alist, 'secret_q2', enc)
    alist = obj_list_decrypt(alist, 'secret_q3', enc)
    alist = obj_list_decrypt(alist, 'secret_a1', enc)
    alist = obj_list_decrypt(alist, 'secret_a2', enc)
    alist = obj_list_decrypt(alist, 'secret_a3', enc)
    alist = obj_list_decrypt(alist, 'memo', enc)
    if sort_proc is None:
        def get_prop_obj(acc, encryptor=enc):
            return obj_decrypt(
                acc.service, 'service_name', encryptor).service_name
        alist = obj_sort_by_proc(alist, get_prop_obj)
    else:
        alist = obj_sort_by_proc(alist, prop_name)
    return alist

