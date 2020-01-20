from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from order.models import Order
from ..utils import get_paginator_items

DASHBOARD_PAGINATE_BY = 30


def order_list(request):
    orders = Order.objects.all()
    orders = get_paginator_items(
        orders,
        DASHBOARD_PAGINATE_BY,
        request.GET.get('page')
    )
    ctx = {'orders': orders}
    return TemplateResponse(
        request,
        'dashboard/orders/list.html',
        ctx,)


def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    ctx = {'order': order}
    return TemplateResponse(request,
                            'dashboard/detail.html',
                            ctx,)
