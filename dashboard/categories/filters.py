from django_filters import (
    FilterSet, CharFilter
)
from product.models import Category
from dron_market2 import widgets
from django.db import models

class CategoryFilter(FilterSet):
    # name = CharFilter(label='name', lookup_expr='icontains', )

    class Meta:
        model = Category
        fields = ['name']
        filter_overrides = {
            models.CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'widget': widgets.WidgetForm
                }
            }
        }
