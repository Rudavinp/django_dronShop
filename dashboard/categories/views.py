from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404

from .filters import CategoryFilter
from ..utils import get_paginator_items
from .forms import CategoryForm
from product.models import Category

DASHBOARD_PAGINATE_BY = 30


def category_list(request):
    categories = Category.tree.root_nodes().order_by('name')
    category_filters = CategoryFilter(request.GET, queryset=categories)
    categories = get_paginator_items(category_filters.qs, DASHBOARD_PAGINATE_BY,
                                     request.GET.get('page'))
    ctx = {'categories': categories, 'filter_set': category_filters,
           'is_empty': not category_filters.queryset.exists()}
    print(23323, categories)
    return TemplateResponse(request, 'dashboard/category/list.html', ctx)


def category_edit(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    parent = get_object_or_404(Category, pk=category.parent_id) if category.get_ancestors() else None
    form = CategoryForm(request.POST or None, instance=category, ancestor=parent)
    if form.is_valid():
        form.save()
        return redirect('dashboard:category-detail', pk=pk)
    ctx = {'category': category, 'form': form}
    return TemplateResponse(request, 'dashboard/category/form.html', ctx)


def category_create(request, root_pk=None):
    ancestor = None
    category = Category()
    if root_pk:
        ancestor = get_object_or_404(Category, pk=root_pk)
    form = CategoryForm(request.POST or None, ancestor=ancestor)
    if form.is_valid():
        form.save()
        if root_pk:
            return redirect('dashboard:category-detail', pk=root_pk)
        return redirect('dashboard:category-list')
    ctx = {'category': category, 'form': form}
    return TemplateResponse(request, 'dashboard/category/form.html', ctx)


def categoty_details(request, pk):
    category = get_object_or_404(Category, pk=pk)
    chieldren = category.get_children()
    ctx = {'category' : category, 'chieldren': chieldren}
    return TemplateResponse(request, 'dashboard/category/detail.html', ctx)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    chieldren = category.get_descendants()
    if request.method == 'POST':
        category.delete()
        if category.parent:
            return redirect('dashboard:category-detail', pk=category.parent.pk)
        return redirect('dashboard:category-list')
    ctx = {
            'category': category,
           'cheildren': chieldren,
           }
    #TODO category.products who deletes
    return TemplateResponse(request, 'dashboard/category/delete.html', ctx)