from django.conf.urls import url
from . import views

# app_name = 'order'
TOKEN_PATTERN = ('(?P<token>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})')
TOKEN_PATER = ('(?P<token>\w+)')

urlpatterns = [
	url(r'^add/(?P<product_id>\w+)/$', views.add_to_cart, name='add_to_cart'),
	url(r'^checkout/$', views.checkout, name='checkout'),
	url(r'^login/$', views.checkout_login, name='login'),
	url(r'^summary/$', views.anonimus_summary, name='summary'),
	url(r'^%s/payment/$' % (TOKEN_PATTERN,), views.payment, name='payment')

	# url(r'^cart/$', views.cart_index, name='cart'),
]

# app_name = 'cart'

cart_urlpatterns = [
	url(r'^$', views.cart_index, name='index'),
	url(r'^update/(?P<product_id>\d+)/$', views.update_product_cart, name='update_product'),
	url(r'^clear-cart/$',views.clear_cart, name='clear-cart')
]

