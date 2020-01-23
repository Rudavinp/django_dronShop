from django import forms
from .models import Cart
from product.forms import ProductForm
from account.models import Address
from discount.models import Coupon
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class CheckoutContactrForm(forms.Form):
	name = forms.CharField(required=True)
	phone = forms.CharField(required=True)


class ChangeQuantityForm(ProductForm):

	def __init__(self, *args, **kwargs):
		self.product = kwargs.pop('product')
		self.cart = kwargs.pop('cart')
		super().__init__(*args, **kwargs)
		self.fields['quantity'].widget.attrs = {
			'min': 2,
		}

	def save(self):
		from .views import save_to_cart
		quantity = self.cleaned_data['quantity']
		save_to_cart(self.cart, self.product, quantity, replace=True)


class NoteCartForm(forms.ModelForm):

	note = forms.CharField(
		max_length=250, required=False, strip=True, label=False,
		widget=forms.Textarea({'rows': 3}),
	    )

	class Meta:
		model = Cart
		fields = ['note', ]


class AnonimusUserEmailForm(forms.ModelForm):

	class Meta:
		model = Cart
		fields = ['email', ]






class AddressForm(forms.ModelForm):

	class Meta:
		model = Address
		exclude = ['street_addres_2',]



class CartCouponForm(forms.Form):

	code = forms.IntegerField()

	def clean(self):
		code = self.cleaned_data.get('code')
		try:
			coupon = Coupon.objects.get(code=code)
		except ObjectDoesNotExist:
			raise forms.ValidationError('Wrong code',)

		if timezone.now().date() > coupon.end_date:
			raise forms.ValidationError('Coupon already not active', )
		elif timezone.now().date() < coupon.start_date:
			raise forms.ValidationError('Coupon not active yet', )
		if not coupon.is_active:
			raise forms.ValidationError('Coupon not active',)
		return code

