from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.category_list, name='category-list'),
    url(r'^add/$', views.category_create, name='category-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.categoty_details, name='category-detail'),
]