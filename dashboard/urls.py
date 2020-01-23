from django.conf.urls import url, include

from . import views
from .products.urls import urlpatterns as products_urls
from .categories.urls import urlpatterns as category_urls
from .staff.urls import urlpatterns as staff_urls
from .orders.urls import urlpatterns as orders_urls
from .discount.urls import urlpatterns_coupons as coupons_urls
from .discount.urls import urlpatterns_sales as sales_urls



urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'products/', include(products_urls)),
	url(r'categories/', include(category_urls)),
	url(r'staff/', include(staff_urls)),
	url(r'orders/', include(orders_urls)),
	url(r'coupons/', include(coupons_urls)),
	url(r'sales/', include(sales_urls))
]