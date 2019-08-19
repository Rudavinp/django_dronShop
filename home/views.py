from django.shortcuts import render
from django.template.response import TemplateResponse
from product.models import Product, ProductImage, Category
from django.utils.functional import lazy
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from dron_market2 import settings

def home(request, product_id=1):
    def func(text):
        return text.title()

    lazy_func = lazy(func, str)

    res = lazy_func('test')
    print(res.find('T'))


    products = ProductImage.objects.filter(is_main=True)
    categoryes = Category.objects.all()
    cat = get_object_or_404(Category, pk=1)
    print(2222, cat)
    # print(products)
    # print('id: ', product_id)
    # print('request: ', list(request))
    # print('static_dir', settings.STATICFILES_DIRS)
    # print('media_dir: ', settings.MEDIA_ROOT)
    # print('tempate_dirs ', settings.TEMPLATES)
    return TemplateResponse(request, 'home/home.html',
                            {'products': products,
                             'categoryes': categoryes,
                             },
                            )

