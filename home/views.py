from django.shortcuts import render
from django.template.response import TemplateResponse
from product.models import Product, ProductImage, Category
from django.utils.functional import lazy
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404

from dron_market2 import settings


def home(request):

    products = ProductImage.objects.filter(is_main=True)

    return TemplateResponse(request, 'home/home.html',
                            {'products': products,
                             },
                            )

