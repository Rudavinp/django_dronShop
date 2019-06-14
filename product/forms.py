from django import forms


class ProductForm(forms.Form):

	quantity = forms.IntegerField(min_value=0,
	                              initial=1, required=False)