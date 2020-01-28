from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product

from core.views import add_product_comment
from dashboard.categories.forms import CategoryForm


def get_product_model():
    return Product.objects.create(name='testProd')


def test_add_product_comment()