def obj_sort_by_lambda(obj_list, lmbd):
    new_obj_list = obj_list.copy()
    new_obj_list.sort(key=lmbd)
    return new_obj_list

def obj_sort_by_property_name(obj_list, prop_name):
    return obj_sort_by_lambda(obj_list, lambda x:getattr(x, prop_name))

def obj_list_decrypt(obj_list, enc):
    new_obj_list = []
    for obj in obj_list:
        new_obj_list.append(obj.decrypt(enc))
    return new_obj_list

