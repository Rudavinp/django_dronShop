from django.forms import ModelForm
from discount.models import Coupon


class CouponForm(ModelForm):

    class Meta:
        model = Coupon
        exclude = []
