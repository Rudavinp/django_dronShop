from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from .forms import ProductForm, CommentForm
from .models import Product, Category
from core.models import Comment
from core.views import add_product_comment
from discount.models import Sale


def product(request, slug, product_id):
	product = Product.objects.get(id=product_id)
	if slug != product.get_slug:
		return HttpResponsePermanentRedirect(product.get_absolute_url())

	comment_form = CommentForm(request.POST or None)
	form = ProductForm(request.POST or None)
	comments = product.comment.filter(is_visible=True)

	ctx = {
		'product': product,
		'form': form,
		'comment_form': comment_form,
		'comments': comments
	}
	return TemplateResponse(request,
							'product/product.html',
							ctx)


def category(request, category_slug):
	products= Product.objects.filter(category__slug=category_slug)
	ctx = {'products': products, }
	return TemplateResponse(request,
	                        'category/category.html',
							ctx
	                        )



def search(request):
	query = request.GET.get('q')
	results = Product.objects.filter(name__icontains=query)
	return TemplateResponse(request, 'search/search_results.html', {'results':results})
