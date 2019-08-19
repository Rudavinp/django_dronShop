from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^(?P<slug>[a-z0-9-]+?)-(?P<product_id>[0-9]+)/$', views.product, name='product'),

	url(r'^(?P<category_slug>)/$', views.category, name='category'),

	url(r'^cart_adding$', views.cart_adding, name='cart_adding')
]