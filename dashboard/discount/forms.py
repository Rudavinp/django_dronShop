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
    coupuns  = forms.ModelMultipleChoiceField(
        queryset=Coupon.objects.all(),
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
        print(34, instance)
        new_products = self.cleaned_data.get('products', [])
        cup = self.cleaned_data.get('coupuns', [])
        print(23, new_products)
        instance.products.set(Product.objects.all())
        prod = Product.objects.get(pk=3)
        print(99, instance.products)
        print(98, prod)
        print(97, prod.sale)
        return instance


