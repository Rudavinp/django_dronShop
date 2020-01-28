
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static
from home.urls import urlpatterns as home_urls
from product.urls import urlpatterns as product_urls
from order.urls import (urlpatterns as order_urls,
                        cart_urlpatterns as cart_urls,
                        )
from account.urls import urlpatterns as account_urls
from dashboard.urls import urlpatterns as dashboard_urls
from core.urls import urlpatterns as core_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(home_urls)),
    path('product/', include((product_urls, 'product'), namespace='product')),
    path('order/', include((order_urls, 'order'), namespace='order')),
    path('account/', include((account_urls, 'account'), namespace='account')),
    path('cart/', include((cart_urls, 'cart'), namespace='cart')),
    path('dashboard/', include((dashboard_urls, 'dashboard'), namespace='dashboard')),
    path('account/', include('social_django.urls', namespace='social')),
    path('core/', include((core_urls, 'core'), namespace='core')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)