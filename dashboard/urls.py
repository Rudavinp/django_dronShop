from django.conf.urls import url, include

from . import views
from .products.urls import urlpatterns as products_urls
from .categories.urls import urlpatterns as category_urls
from .staff.urls import urlpatterns as staff_urls
from .orders.urls import urlpatterns as orders_urls


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'products/', include(products_urls)),
	url(r'categories/', include(category_urls)),
	url(r'staff/', include(staff_urls)),
	url(r'orders/', include(orders_urls))
]