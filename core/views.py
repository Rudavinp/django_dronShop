from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required

from product.models import Product
from product.forms import CommentForm
from .models import Comment
from .utils import test_user_is_auth


@test_user_is_auth
def add_product_comment(request, prod_id, comment_id=None):
    print(11111111111111111111111111)
    product = Product.objects.get(pk=prod_id)
    print(1, product)
    form = CommentForm(request.POST)
    print(2, form)
    print(21, request.POST)
    if form.is_valid():
        print(3)
        text = form.cleaned_data['text']
        comment, _ = Comment.objects.get_or_create(pk=comment_id, product=product,
                                                   user=request.user)
        comment.text = text
        comment.save()
    return HttpResponsePermanentRedirect(product.get_absolute_url())
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
