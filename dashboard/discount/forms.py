from django.forms import ModelForm
from discount.models import Coupon, Sale


class CouponForm(ModelForm):

    class Meta:
        model = Coupon
        exclude = []


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        exclude = []