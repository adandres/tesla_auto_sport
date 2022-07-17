from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('single_profile', request.user.id)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Vous n\'êtes pas autorisés à voir cette page')
        return wrapper_func
    return decorator
