from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def staff_required(view_func):
    """Allow only staff/superuser access to platform admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Access denied. Staff only.')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper
