from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.order_list, name='orders-list'),
    url(r'^(?P<order_pk>[0-9]+)/$', views.order_details,
        name='order-details'),
    url(r'^(?P<order_pk>[0-9]+)/delete/$', views.order_delete,
        name='order-delete'),
    url(r'^download-csv/(?P<order_pk>[0-9]+)/$', views.to_csv, name='to-csv'),
]