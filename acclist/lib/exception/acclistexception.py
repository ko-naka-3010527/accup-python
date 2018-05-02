import json

class AcclistException(Exception):
    def set_params(self, err_dict, py_e="", opt_msg=""):
        self.acclist_err_dict = err_dict
        self.acclist_err_dict['py_e'] = py_e
        self.acclist_code = err_dict['code']
        self.acclist_message = err_dict['message']
        self.py_e = py_e
        self.opt_msg = opt_msg

