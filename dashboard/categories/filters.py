from django_filters import (
    FilterSet, CharFilter
)
from product.models import Category


class CategoryFilter(FilterSet):
    name = CharFilter(label='name', lookup_expr='incontains')

    class Meta:
        model = Category
        fields = []