from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from .models import ProductInCart, ProductInOrder, Order
from .forms import CheckoutContactrForm, ChangeQuantityForm, NoteCartForm, AnonimusUserEmailForm, AddressForm, CartCouponForm
from django.contrib.auth.models import User
from .models import Cart, Product
from product import views
from product.forms import ProductForm
from account.forms import LoginForm
from django.db.models import Sum
from .utils import get_cart_from_request, change_billing_address_in_cart, get_client_id
from .task import send_order_message
from discount.models import Coupon
from decimal import Decimal

COOKIE_NAME = 'cart'
# def cart_adding(request):
# 	return_dict = {}
# 	session_key = request.session.session_key
# 	print('----------------')
# 	print('POST', request.POST)
# 	data = request.POST
# 	product_id =  data.get('product_id')
# 	nmb = data.get('nmb')
# 	print('pre_new_product')
# 	new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, product_id=product_id,
# 	                                                             is_active=True, defaults={"nmb": nmb})
# 	# new_product = ProductInCart.objects.create(session_key=session_key, product_id=product_id, nmb=nmb)
# 	# Как он создает новый объект оп ID
# 	# Откуда берутся данные в POSTе - данные передает ajax()
# 	# Узнать подробней про метод action
# 	if not created:
# 		print("not created")
# 		new_product.nmb += int(nmb)
# 		new_product.save(force_update=True)
#
# 	product_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
# 	product_total_nmb = product_in_cart.count()
# 	# Остановился здесь!
#
# 	return_dict['product_total_nmb'] = product_total_nmb
# 	return_dict['products'] = []
#
# 	for item in product_in_cart:
# 		product_dict = dict()
# 		product_dict["id"] = item.id
# 		product_dict["name"] = item.product.name
# 		product_dict["price_per_item"] = item.price_per_item
# 		product_dict["nmb"] = item.nmb
# 		product_dict['total_price'] = item.total_price
# 		return_dict["products"].append(product_dict)
#
#
# 	return JsonResponse(return_dict)


# class EmailAutocomplete(autocomplete.Select2QuerySetView):
# 	pass


def checkout(request):
	session_key = request.session.session_key
	product_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
	form = CheckoutContactrForm(request.POST or None)
	if request.POST:
		if form.is_valid():
			data = request.POST
			name = data.get('name', 'anonimus')
			phone = data['phone']
			user, created = User.objects.get_or_create(username=phone, defaults={'first_name': name})
			order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=3)
			for name, value in data.items():
				if name.startswith('product_in_cart_'):
					product_in_cart_id = name.split("product_in_cart_")[1]
					product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
					product_in_cart.order = order
					product_in_cart.nmb = value
					product_in_cart.save(force_update=True)
					ProductInOrder.objects.create(product=product_in_cart.product,
					                              nmb=product_in_cart.nmb,
					                              price_per_item=product_in_cart.price_per_item,
					                              total_price=product_in_cart.total_price,
					                              order=order,)
	return render(request, 'orders/checkout.html', locals())


def set_cart_cookie(cart, response):
	response.set_signed_cookie('cart', cart.token)


def get_or_create_cart(request):
	if request.user.is_authenticated:
		cart_queryset = Cart.objects.all()
		return cart_queryset.get_or_create(user=request.user)[0]
	token = request.get_signed_cookie(COOKIE_NAME, default=None)
	return Cart.objects.all().filter(token=token, user=None).get_or_create(
		defaults={'user': None})[0]





def cart_index(request):
	products_for_cart = []
	code = 0
	cart = get_cart_from_request(request)
	if cart is None:
		cart = Cart()
	products = cart.product_in_cart.all()
	for product in products:
		form = ChangeQuantityForm(None, cart=cart, product=product)
		products_for_cart.append({ 'quantity': product.quantity,
		                           'product': product.product,
		                           'price': product.product.price,
		                           'total_price': product.get_total_price(),
		                           'form': form,})

	form_coupon = CartCouponForm(request.POST or None)

	total_price = cart.get_total()
	ctx = {
		'product': products_for_cart,
	    'total_price': total_price,
		'form_coupon': form_coupon,
		'code': code
	}
	return TemplateResponse(request, 'orders/index.html', ctx)


def save_to_cart(cart, product, quantity, replace=False):

	product, _ = cart.product_in_cart.get_or_create(product=product,
	                                                defaults={'quantity':0})
	if not replace:
		new_quantity = quantity + product.quantity
	else:
		new_quantity = quantity
	product.quantity = new_quantity
	product.save(update_fields=['quantity'])
	total_price = cart.product_in_cart.aggregate(total_quantity=Sum('quantity'))['total_quantity']
	if not total_price:
		total_price = 0
	cart.quantity = total_price
	cart.save(update_fields=['quantity'])


def add_to_cart(request, product_id):
	products = Product.objects.all()
	product = get_object_or_404(products, pk=product_id)
	response = views.product(request, product.get_slug,  product_id)
	cart = get_or_create_cart(request)
	form = ProductForm(request.POST)
	if form.is_valid():
		quantity = form.cleaned_data['quantity']
		if not form.cleaned_data['quantity']:
			quantity = 1
		save_to_cart(cart, product, quantity)
	if not request.user.is_authenticated:
		set_cart_cookie(cart, response)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_product_cart(request, product_id):
	cart = get_cart_from_request(request)

	product = get_object_or_404(Product, pk=product_id)
	form = ChangeQuantityForm(request.POST, cart=cart, product=product)
	if form.is_valid():
		form.save()
		response = {
			'cart': {
				'numItems': cart.quantity,
				'numProduct': len(cart)
			}
		}
	return redirect('cart:index')


def apply_discount_cart(request, code):
	"""Применяет скидку к общей сумме товаров в корзине"""
	if not code:
		return redirect('cart:index')
	form_coupon = CartCouponForm(request.POST or None)
	if form_coupon.is_valid():
		coupon = Coupon.objects.get(code=int(request.POST['code']))
		discount = Decimal(1 - coupon.discount / 100)
		cart = get_cart_from_request(request)
		cart.discount = discount
		cart.save()
		return redirect('cart:index')
	return (cart_index(request))

def clear_cart(request):
	cart = get_or_create_cart(request)
	cart.product_in_cart.all().delete()
	return cart_index(request)


def checkout_login(request):
	ctx = {'form': LoginForm()}
	return TemplateResponse(request, 'orders/login.html', ctx)


def _fill_order_with_cart_data(order, cart):

	"""Заполняет заказ продуктами из корзины"""

	from .utils import add_varian_to_order
	for line in cart:
		add_varian_to_order(
			order, line.product,
			line.quantity, line.get_total_price()
		)
	if cart.note:
		order.costume_note = cart.note
		order.save(update_fields=['customer_note'])



def handle_order(request, cart):
	"""Создает заказ"""
	order_data = {}
	total = cart.get_total()
	order_data.update({'user': cart.user,
						'user_email': cart.email,
						'billing_address': cart.billing_address,
						'total': total,
						'tracking_client_id': get_client_id(request)
						})
	order = Order.objects.create(**order_data)
	_fill_order_with_cart_data(order, cart)

	if not order:
		return redirect('chaeckout:summary')
	cart.delete()
	send_order_message.delay(order.id)
	return redirect('order:payment', token=order.token)


def anonimus_summary(request):
	"""Выводит форму для создания заказа"""
	cart = get_or_create_cart(request)
	init_email = ''
	if request.user.is_authenticated:
		init_email = request.user.email
	note_form = NoteCartForm(request.POST or None, instance=cart)
	user_form = AnonimusUserEmailForm(request.POST or None, initial={'email': init_email}, instance=cart)
	address_form = AddressForm(request.POST or None)

	if user_form.is_valid() and address_form.is_valid():
		user_form.save()
		address = address_form.save()
		change_billing_address_in_cart(cart, address)
		return handle_order(request, cart)

	ctx = {
		'note_form': note_form,
		'user_form': user_form,
		'address_form': address_form,
	}
	return TemplateResponse(request, 'orders/summary_anonimus.html', ctx)


def payment(request, token):

	orders = Order.objects.filter(token=token)
	order = get_object_or_404(orders, token=token)
	ctx = {
		'order': order,
	}
	return TemplateResponse(request, 'orders/payment.html', ctx)