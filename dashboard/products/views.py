from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import permission_required

from ..utils import get_paginator_items
from product.models import Product, Attribute, AttributeValue, ProductType, Category, ProductImage
from .filters import FilterSet, ProductFilter
from . import forms


DASHBOARD_PAGINATE_BY = 10

# @permission_required('product.manage_product', login_url='/')
def product_list(request):
    products = Product.objects.all()
    product_type = ProductType.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = get_paginator_items(products, DASHBOARD_PAGINATE_BY,
                                   request.GET.get('page'))
    ctx = {
        'products': products,
        'filter_set': product_filter,
        'product_types': product_type
    }
    return TemplateResponse(request, 'dashboard/products/list.html', ctx)


def product_detail(request, pk):
    products = Product.objects.all()
    product = get_object_or_404(products, pk=pk)
    variants = []
    ctx = {'product': product,
           'variants': variants,}
    return TemplateResponse(request, 'dashboard/products/detail.html', ctx )


def product_choice_type(request):
    form = forms.ProductChoiceTypeForm(request.POST or None)
    if form.is_valid():
        redirect_url = reverse('dashboard:product-add', kwargs={'type_pk': form.cleaned_data['types'].pk})
        return redirect(redirect_url)
    ctx = {'form': form}
    return TemplateResponse(request, 'dashboard/products/modal/select_type.html', ctx)


def product_create(request, type_pk=None):
    product_type = get_object_or_404(ProductType, pk=type_pk)
    product = Product()
    print(2222, product.pk)
    product.product_type = product_type
    form = forms.ProductForm( request.POST or None, instance=product)
    if form.is_valid():
        product = form.save()
        return redirect('dashboard:product-details', pk=product.pk)
    else:
        print('error', form.errors)
    ctx = {'product_form': form, 'product': product}
    return TemplateResponse(request, 'dashboard/products/form1.html', ctx)


def product_images_list(request, prod_pk):
    product = get_object_or_404(Product, pk=prod_pk)
    images = product.images.all()
    for image in images:
        print(11111, image.image)
    ctx = {'images': images, 'product': product}
    return TemplateResponse(request, 'dashboard/product_image/list.html', ctx)


def product_image_add(request, prod_pk):
    product = get_object_or_404(Product, pk=prod_pk)
    product_image = ProductImage(product=product)
    form = forms.ProductImageForm(request.POST or None, request.FILES or None, instance=product_image)
    if form.is_valid():
        form.save()
        print(11111, product.get_image())
        return redirect('dashboard:product-images-list', prod_pk=product.pk)
    ctx = {'image_form':form, 'product':product}
    return TemplateResponse(request, 'dashboard/product_image/form.html', ctx)


def product_image_delete(request, image_pk):
    product_image = get_object_or_404(ProductImage, pk=image_pk)
    if request.method == 'POST':
        product_image.delete()
        return redirect('dashboard:product-list')
    return TemplateResponse(request, 'dashboard/product_image/delete.html', {'product_image':product_image})



def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = forms.ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        product = form.save()
        return redirect('dashboard:product-details', pk=product.pk)
    ctx = {'product-form': form, 'product': product}
    return TemplateResponse(request, 'dashboard/products/form1.html', ctx)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:product-list')
    return TemplateResponse(request, 'dashboard/products/delete.html', {'product':product})


def product_type_list(request):
    types = ProductType.objects.all().prefetch_related('attribute').order_by('name')
    types_filter = None
    product_types = [(types.pk, types.name, types.attribute.all()) for types in types ]
    ctx = {
        'product_types': product_types, 'not_empty': True,
    }

    return TemplateResponse(request, 'dashboard/product_type/list.html', ctx)


def product_type_add(request):
    product_type = ProductType()
    form = forms.ProductTypeForm(request.POST or None, instance=product_type)
    if form.is_valid():
        form.save()
        return redirect('dashboard:product-type-list')
    ctx = {'form':form, 'product_type':product_type}
    return TemplateResponse(request, 'dashboard/product_type/form.html', ctx)


def product_type_edit(request, pk):
    product_type = get_object_or_404(ProductType, pk=pk)
    form = forms.ProductTypeForm(request.POST or None, instance=product_type)
    if form.is_valid():
        form.save()
        return redirect('dashboard:product-type-list')
    ctx = {'form':form, 'product_type':product_type}
    return TemplateResponse(request, 'dashboard/product_type/form.html', ctx)


def product_type_delete(request, pk):
    product_type = get_object_or_404(ProductType, pk=pk)
    if request.method == 'POST':
        product_type.delete()
        return redirect('dashboard:product-type-list')
    ctx = {'product_type': product_type,
           'product': product_type.products.all()}
    return TemplateResponse(request, 'dashboard/product_type/modal/confirm_delete.html', ctx)



def attributes_list(request):
    attributes = Attribute.objects.prefetch_related('attribute_value')
    attributes = [(attribute.pk, attribute.name, attribute.attribute_value.all()) for attribute in attributes]
    ctx = {'attributes': attributes}
    return TemplateResponse(request, 'dashboard/attributes/list.html', ctx)


def attribute_details(request, pk):
    attributes = Attribute.objects.prefetch_related('attribute_value').all()
    attribute = get_object_or_404(attributes, pk=pk)
    values = attribute.attribute_value.all()
    ctx = {'attribute': attribute, 'values': values, }
    return TemplateResponse(request, 'dashboard/attributes/detail.html', ctx)


def attribute_add(request):
    attribute =Attribute()
    form = forms.AttributeForm(request.POST or None, instance=attribute)
    if form.is_valid():
        attribute = form.save()
        return redirect('dashboard:attribute-detail', pk=attribute.pk)
    ctx = {'attribute': attribute, 'form': form}
    return TemplateResponse(request, 'dashboard/attributes/form.html', ctx)


def attribute_value_add(request, attribute_pk):
    attribute = get_object_or_404(Attribute, pk=attribute_pk)
    value = AttributeValue(attribute_id=attribute_pk)
    form = forms.AttributeValueForm(request.POST or None, instance=value)
    if form.is_valid():
        form.save()
        return redirect('dashboard:attribute-detail', pk=attribute.pk)
    ctx = {'attribute': attribute, 'value': value, 'form':form}
    return TemplateResponse(request, 'dashboard/attributes/value/form.html', ctx)


