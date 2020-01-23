from django.conf.urls import url
from . import views

urlpatterns_coupons = [
    url(r'^$', views.coupons_list, name='coupons-list'),
    url(r'^(?P<coupon_pk>[0-9]+)/$', views.coupon_details,
        name='coupon-details'),
    url(r'^add/(?P<pk>[0-9]+)?/$', views.coupon_create, name='coupon-add'),
]

urlpatterns_sales = [
    url(r'^$', views.sales_list, name='sales-list'),
    url(r'^(?P<sale_pk>[0-9]+)/$', views.sale_details,
        name='sale-details'),
    url(r'^add/(?P<pk>[0-9]+)?/$', views.sale_create, name='sale-add'),
]