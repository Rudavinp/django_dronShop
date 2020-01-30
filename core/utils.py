from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect


def requare_user_auth(func):
    def _wrap_func(request, *args, **kwargs):
        print(66666)

        if request.user.is_authenticated:
            return (func(request, *args, **kwargs))
        messages.error(request, 'You need to authenticate')
        #TODO: How messages adds to template?
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return _wrap_func