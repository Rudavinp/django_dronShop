from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^comment/(?P<prod_id>[0-9]+)/$',
            views.add_product_comment, name='comment'),
]