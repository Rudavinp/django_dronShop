from django.shortcuts import render
from django.template.response import TemplateResponse
from product.models import Product, ProductImage, Category

from dron_market2 import settings

def home(request, product_id=1):
	products = ProductImage.objects.filter(is_main=True)
	categoryes = Category.objects.all()
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

