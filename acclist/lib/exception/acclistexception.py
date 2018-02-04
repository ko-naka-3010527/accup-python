import json

class AcclistException(Exception):
    def __init__(self, err_dict, py_e="", opt_msg=""):
        self.code = err_dict['code']
        self.message = err_dict['message']
        self.py_e = py_e
        self.opt_msg = opt_msg

    def __str__():
        return json.dumps({
            "code": self.code,
            "message": self.message + (
                "(" + self.opt_msg + ")" if len(self.opt_msg) > 0 else ""
            ),
            "python_error": self.py_e,
        })

