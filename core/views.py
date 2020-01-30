from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from product.models import Product
from product.forms import CommentForm
from .models import Comment
from .utils import requare_user_auth


@requare_user_auth
def add_product_comment(request, prod_id, comment_id=None):
    print(1222)
    product = Product.objects.get(pk=prod_id)
    # instance=None
    # if comment_id:
    # #     instance = Comment.objects.get(pk=comment_id)
    #     print(22222, instance, request.POST)
    comment, _ = Comment.objects.get_or_create(pk=comment_id, product=product,
                                               user=request.user)
    form = CommentForm(request.POST, instance=comment)
    print(2222, form)
    print(3333, comment)
    if form.is_valid():
        text = form.cleaned_data['text']
        # comment, _ = Comment.objects.get_or_create(pk=comment_id, product=product,
        #                                            user=request.user)
        comment.text = text
        comment.save()
    return redirect(product.get_absolute_url())

#TODO: func -> user can edit and delete his comments

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
