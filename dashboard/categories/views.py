from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404

from .filters import CategoryFilter
from ..utils import get_paginator_items
from .forms import CategoryForm
from product.models import Category

DASHBOARD_PAGINATE_BY = 30


def category_list(request):
    categories = Category.tree.root_nodes().order_by('name')
    print(555, request.GET)
    category_filters = CategoryFilter(request.GET, queryset=categories)
    print(1111, category_filters.qs)
    categories = get_paginator_items(category_filters.qs, DASHBOARD_PAGINATE_BY,
                                     request.GET.get('page'))
    print(22, categories.object_list)
    ctx = {'categories': categories, 'filter_set': category_filters,
           'is_empty': not category_filters.queryset.exists()}
    return TemplateResponse(request, 'dashboard/category/list.html', ctx)


def category_edit(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('dashboard:category-detail', pk=pk)
    ctx = {'category': category, 'form': form}
    return TemplateResponse(request, 'dashboard/category/form.html', ctx)



def category_create(request):
    category = Category()
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard:category-list')
    ctx = {'category': category, 'form': form}
    return TemplateResponse(request, 'dashboard/category/form.html', ctx)


def categoty_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    ctx = {'category' : category}
    return TemplateResponse(request, 'dashboard/category/detail.html', ctx)