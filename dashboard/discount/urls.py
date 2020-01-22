from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.coupons_list, name='coupons-list'),
    url(r'^(?P<coupon_pk>[0-9]+)/$', views.coupon_details,
        name='coupon-details'),
    url(r'^add/(?P<pk>[0-9]+)?/$', views.coupon_create, name='coupon-add'),


]