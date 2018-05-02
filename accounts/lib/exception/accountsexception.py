import json

class AccountsException(Exception):
    def set_params(self, err_dict, py_e="", opt_msg=""):
        self.accounts_err_dict = err_dict
        self.accounts_err_dict['py_e'] = py_e
        self.accounts_code = err_dict['code']
        self.accounts_message = err_dict['message']
        self.py_e = py_e
        self.opt_msg = opt_msg

