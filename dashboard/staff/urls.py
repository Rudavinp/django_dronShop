from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.staff_list, name='staff-list'),
    url(r'^(?P<staff_pk>[0-9]+)/$', views.staff_detail, name='staff-detail'),
]
