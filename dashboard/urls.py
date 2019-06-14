from django.conf.urls import url, include

from . import views
from .products.urls import urlpatterns as products_urls
from .categories.urls import urlpatterns as category_urls


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'products/', include(products_urls)),
	url(r'categories/', include(category_urls)),
]