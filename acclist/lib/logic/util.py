def create_error_message(msg, fmt):
    if fmt == 'html':
        return '<span class="accup_errormsg">' + msg + '</span><br>' + "\n"
    elif fmt == 'json':
        return msg + ';'
    else:
        return msg + "\n"

