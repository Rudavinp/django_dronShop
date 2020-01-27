from django import forms
from discount.models import Coupon, Sale
from product.models import Product


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        exclude = []


class SaleForm(forms.ModelForm):

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False,
    )

    class Meta:
        model = Sale
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'].queryset = Product.objects.all()

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        new_products = self.cleaned_data.get('products', [])
        instance.products.set(new_products)
        return instance


