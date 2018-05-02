from django.core.exceptions import PermissionDenied

def is_users_url(user, url_username, raise_exception=True):
    if user.username != url_username:
        if raise_exception:
            raise PermissionDenied
        else:
            return False
    return True

