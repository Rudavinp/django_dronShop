from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from ..utils import get_paginator_items
from product.models import Product, Attribute, AttributeValue, ProductType, Category
from .filters import FilterSet, ProductFilter
from . import forms


DASHBOARD_PAGINATE_BY = 10


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
    print( 3333, product.product_type)
    print( 334434, ProductType.objects.get(products__pk=pk).attribute)
    return TemplateResponse(request, 'dashboard/products/detail.html', ctx )


def product_choice_type(request):
    form = forms.ProductChoiceTypeForm(request.POST or None)
    if form.is_valid():
        redirect_url = reverse('dashboard:product-add', kwargs={'type_pk': form.cleaned_data['types'].pk})
        return redirect(redirect_url)
    ctx = {'form': form}
    return TemplateResponse(request, 'dashboard/products/modal/select_type.html', ctx)


def product_create(request, type_pk):
    product_type = get_object_or_404(ProductType, pk=type_pk)
    product = Product()
    product.product_type = product_type
    form = forms.ProductForm( request.POST or None, instance=product)
    if form.is_valid():
        product = form.save()
        return redirect('dashboard:product-details', pk=product.pk)
    else:
        print('error', form.errors)
    ctx = {'product_form': form, 'product': product}
    return TemplateResponse(request, 'dashboard/products/form1.html', ctx)


def prduct_type_list(request):
    types = ProductType.objects.all().prefetch_related('attribute').order_by('name')
    types_filter = None
    product_types = [(types.pk, types.name, types.attribute.all()) for types in types ]
    ctx = {
        'product_types': product_types, 'not_empty': True,
    }
    print(123, types)
    for i in product_types:
        print(1, i)
    return TemplateResponse(request, 'dashboard/product_type/list.html', ctx)


def product_type_add(request):
    print('lol')
    product_type = ProductType()
    form = forms.ProductTypeForm(request.POST or None, instance=product_type)
    if form.is_valid():
        form.save()
        return redirect('dashboard:product-type-list')
    ctx = {'form':form, 'product_type':product_type}
    print(11111111111111111111111)
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
    print(11111)
    attributes = Attribute.objects.prefetch_related('attribute_value')
    print(222, attributes)
    for attribute in attributes:
        print(1212, attribute)
    attributes = [(attribute.pk, attribute.name, attribute.attribute_value.all()) for attribute in attributes]
    ctx = {'attributes': attributes}
    return TemplateResponse(request, 'dashboard/attributes/list.html', ctx)


def attribute_details(request, pk):
    attributes = Attribute.objects.prefetch_related('attribute_value').all()
    attribute = get_object_or_404(attributes, pk=pk)
    values = attribute.attribute_value.all()
    print(11,attribute.__dict__)
    for value in values:
        print(22, value.__dict__)
    ctx = {'attribute': attribute, 'values': values, }
    print(222222, values)
    t = TemplateResponse(request, 'dashboard/attributes/detail.html', ctx)
    t.render()
    print(111, t.content)
    return TemplateResponse(request, 'dashboard/attributes/detail.html', ctx)


def attribute_add(request):
    attribute =Attribute()
    form = forms.AttributeForm(request.POST or None, instance=attribute)
    if form.is_valid():
        attribute = form.save()
        return redirect('dashboard:attribute-detail', pk=attribute.pk)
    print('111', form.errors)
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


