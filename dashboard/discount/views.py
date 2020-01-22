from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .forms import CouponForm


from discount.models import Coupon
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
        'dashboard/discount/list.html',
        ctx,)


def coupon_details(request, coupon_pk):
    coupon = get_object_or_404(Coupon, pk=coupon_pk)
    ctx = {'coupon': coupon}
    return TemplateResponse(request,
                            'dashboard/discount/details.html',
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
    return TemplateResponse(request, 'dashboard/discount/form.html', ctx)


