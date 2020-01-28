from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect


def test_user_is_auth(func):
    def _wrap_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return (func(request, *args, **kwargs))
        messages.error(request, 'You need to authenticate')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return _wrap_func