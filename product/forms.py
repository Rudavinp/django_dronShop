from django import forms
from django.contrib.auth.decorators import permission_required
from .models import Product


class ProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=0,
	                              initial=1, required=False)

class SearchForm(forms.Form):
	pass