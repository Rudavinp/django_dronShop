from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

import csv

from order.models import Order
from ..utils import get_paginator_items



DASHBOARD_PAGINATE_BY = 30


def order_list(request):
    orders = Order.objects.all()
    paginate_orders = get_paginator_items(
        orders,
        DASHBOARD_PAGINATE_BY,
        request.GET.get('page')
    )
    ctx = {'orders': orders, 'paginate': paginate_orders}
    return TemplateResponse(
        request,
        'dashboard/orders/list.html',
        ctx,)


def to_csv(request, order_pk):
    order = Order.objects.get(pk=order_pk)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow([f.name for f in Order._meta.get_fields() if not f.many_to_one
                     and not f.one_to_many])

    writer.writerow([order.pk, order.status, order.created.strftime('%d/%m/%Y'),
                    order.tracking_client_id, order.user_email, order.token,
                    order.total])
    return response


def order_details(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    ctx = {'order': order}
    return TemplateResponse(request,
                            'dashboard/orders/details.html',
                            ctx,)


def order_delete(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard:orders-list')
    ctx = {'order': order}
    return TemplateResponse(request, 'dashboard/orders/delete.html', ctx)