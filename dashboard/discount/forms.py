from django import forms
from discount.models import Coupon, Sale
from product.models import Product


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        exclude = []


class SaleForm(forms.ModelForm):

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all().filter(sale=None)
    )

    class Meta:
        model = Sale
        exclude = []

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #