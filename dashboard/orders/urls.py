from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.order_list, name='orders-list')
]