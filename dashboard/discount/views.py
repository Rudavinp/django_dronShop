from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .forms import CouponForm, SaleForm
from product.models import Product

from discount.models import Coupon, Sale
from ..utils import get_paginator_items

DASHBOARD_PAGINATE_BY = 30


def coupons_list(request):
    coupons = Coupon.objects.all()
    paginate_coupons = get_paginator_items(
        coupons,
        DASHBOARD_PAGINATE_BY,
        request.GET.get('page')
    )
    ctx = {'coupons': coupons, 'paginate': paginate_coupons}
    return TemplateResponse(
        request,
        'dashboard/discount/coupons/list.html',
        ctx,)


def coupon_details(request, coupon_pk):
    coupon = get_object_or_404(Coupon, pk=coupon_pk)
    ctx = {'coupon': coupon}
    return TemplateResponse(request,
                            'dashboard/discount/coupons/details.html',
                            ctx,)


def coupon_create(request, pk=None):
    coupon = None
    if pk:
        coupon = get_object_or_404(Coupon, pk=pk)
    form = CouponForm(request.POST or None, instance=coupon)
    if form.is_valid():
        form.save()
        return redirect('dashboard:coupons-list')
    ctx = {'form': form}
    return TemplateResponse(request, 'dashboard/discount/coupons/form.html', ctx)


def sales_list(request):
    sales = Sale.objects.all()
    paginate_sales = get_paginator_items(
        sales,
        DASHBOARD_PAGINATE_BY,
        request.GET.get('page')
    )
    ctx = {'sales': sales, 'paginate': paginate_sales}
    return TemplateResponse(
        request,
        'dashboard/discount/sales/list.html',
        ctx,)


def sale_details(request, sale_pk):
    sale = get_object_or_404(Sale, pk=sale_pk)
    print(sale.products.all())
    ctx = {'sale': sale}
    return TemplateResponse(request,
                            'dashboard/discount/sales/details.html',
                            ctx,)


def sale_create(request, pk=None):
    sale = None
    products = Product.objects.all().filter(sale=None)
    print(23, products)
    if pk:
        sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    if form.is_valid():
        form.save()
        return redirect('dashboard:sales-list')
    ctx = {'form': form}
    return TemplateResponse(request, 'dashboard/discount/sales/form.html', ctx)
