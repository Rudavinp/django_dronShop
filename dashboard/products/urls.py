from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.product_list, name='product-list'),
	url(r'^(?P<pk>[0-9]+)/$', views.product_detail, name='product-details'),
	url(r'^add/select_type/$', views.product_choice_type, name='product-add-select-type'),
	url(r'^add/(?P<type_pk>[0-9]+)/$', views.product_create, name='product-add'),


	url(r'product_type/$', views.prduct_type_list, name='product-type-list'),
	url(r'product_type/add/$', views.product_type_add, name='product-type-add'),
	url(r'product_type/(?P<pk>[0-9]+)/update/$', views.product_type_edit, name='product-type-update'),
	url(r'product_type/(?P<pk>[0-9]+)/delete/$', views.product_type_delete, name='product-type-delete'),

	url(r'attributes/$', views.attributes_list, name='attributes-list'),
	url(r'attributes/add/$', views.attribute_add, name='attribute-add'),
	url(r'attributes/(?P<pk>[0-9]+)/$', views.attribute_details, name='attribute-detail'),
    url(r'attributes/(?P<attribute_pk>[0-9]+)/value/add/$', views.attribute_value_add, name='attribute-value-add')

]