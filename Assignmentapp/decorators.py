from django.http import HttpResponse
from django.shortcuts import redirect


def adminteacher_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.user_role == '3':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('<h1>Access Denied</h1>')

    return wrapper_func


def student_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.user_role == '3':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('studentindex')

    return wrapper_func


def student_profile_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.id == kwargs['stid']:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('<h1>Access Denied</h1>')

    return wrapper_func

def student_editprofile_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.id == kwargs['estid']:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('<h1>Access Denied</h1>')

    return wrapper_func