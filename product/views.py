from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponsePermanentRedirect
from .forms import ProductForm
from .models import Product, Category


def product(request, slug, product_id):
	print(1234455, type(request), request.COOKIES)
	product = Product.objects.get(id=product_id)
	if slug != product.get_slug:
		return HttpResponsePermanentRedirect(product.get_absolute_url())
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	form = ProductForm(request.POST)
	return TemplateResponse(
		request,
		'product/product.html',
		{'product': product,
		 'form': form}
	)


def category(request, category_slug):
	products= Product.objects.filter(category__slug=category_slug)

	return TemplateResponse(request,
	                        'category/category.html',
	                        {'products': products, },
	                        )


# def cart_adding(request):
# 	user = request.user
# 	response = redirect('cart:cart')
# 	return response


def search(request):
	query = request.GET.get('q')
	results = Product.objects.filter(name__icontains=query)
	return TemplateResponse(request, 'search/search_results.html', {'results':results})
