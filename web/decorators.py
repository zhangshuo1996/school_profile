from flask import abort
from functools import wraps

from flask_login import current_user


def permission_required(permission_name):
    """
    验证权限
    :param permission_name: 权限名称
    :return:
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator
