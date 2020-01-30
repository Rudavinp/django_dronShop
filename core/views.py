from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from product.models import Product
from product.forms import CommentForm
from .models import Comment
from .utils import requare_user_auth


@requare_user_auth
def add_product_comment(request, prod_id, comment_id=None):

    # TODO: func -> user can edit and delete his comments
    """Создает новый комментарий под породуктом, если пользователь
    авторизован и перенаправляет обратно на страницу продукта.

    Не реалезованно: передача существующего коментария для его
    редоктирования"""

    product = Product.objects.get(pk=prod_id)
    comment, _ = Comment.objects.get_or_create(pk=comment_id, product=product,
                                               user=request.user)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        text = form.cleaned_data['text']
        # comment, _ = Comment.objects.get_or_create(pk=comment_id, product=product,
        #                                            user=request.user)
        comment.text = text
        comment.save()
    return redirect(product.get_absolute_url())


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
