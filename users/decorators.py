from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles):
    """
    Membatasi akses view berdasarkan role user.
    Contoh: @role_required(['gurubk', 'admin'])
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, "profile"):
                raise PermissionDenied

            if request.user.profile.role not in allowed_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
