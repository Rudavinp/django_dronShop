from django_filters import (
                            FilterSet, CharFilter, ModelMultipleChoiceFilter,
                            ChoiceFilter,
)
from django import forms
from product.models import Category, Product

PUBLISHED_CHOICE = (
    ('1', 'Published'),
    ('0', 'Not published')
)


class ProductFilter(FilterSet):
    name = CharFilter(
                    label='Name',
                    lookup_expr='icontains',
)
    category = ModelMultipleChoiceFilter(label='Category',
                                         field_name='category',
                                         queryset=Category.objects.all(),
                                         )
    is_publisged = ChoiceFilter(
        label='Is published',
        choices=PUBLISHED_CHOICE,
        empty_label='All',
        widget=forms.Select,
    )

    class Meta:
        model = Product
        fields = []

