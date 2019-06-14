import uuid
from order.models import Cart, OrderLine

COOKIE_NAME = 'cart'
FINGERPRINT_PARTS = [
    'HTTP_ACCEPT_ENCODING',
    'HTTP_ACCEPT_LANGUAGE',
    'HTTP_USER_AGENT',
    'HTTP_X_FORWARDED_FOR',
    'REMOTE_ADDR']

UUID_NAMESPACE = uuid.UUID('fb4abc05-e2fb-4e3e-8b78-28037ef7d07f')


def get_client_id(request):
	parts = [request.META.get(key, '') for key in FINGERPRINT_PARTS]
	name = '_'.join(parts)

	return uuid.uuid5(UUID_NAMESPACE, name)


def get_cart_from_request(request):

	"""Получить корзину из запрос (анонима или юзера)"""

	cart_queryset = Cart.objects.all()
	if request.user.is_authenticated:
		cart = cart_queryset.filter(user=request.user).first()
	else:
		token = request.get_signed_cookie(COOKIE_NAME, default=None)
		cart = Cart.objects.all().filter(token=token, user=None).first()
	return cart


def _chek_new_cart_address(cart, address):

	"""Проверяет были ли изменения а адресе
	и нужно ли удалить старый адрес"""

	old_address = cart.billing_address

	has_address_change = any([
		not address and old_address,
		address and not old_address,
		address and old_address and address != old_address
	])

	remove_old_address = (
		has_address_change and
	    old_address is not None and
		(not cart.user or old_address not in cart.user.addresses.all())
	)

	return has_address_change, remove_old_address


def change_billing_address_in_cart(cart, address):

	"""Изменяет или добавляет адресс доставки в корзину
	при совершении заказа """

	change, remove = _chek_new_cart_address(cart, address)

	if change:
			if remove:
				cart.billing_address.delete()
			cart.billing_address = address
			cart.save(update_fields=['billing_address'])


def add_varian_to_order(order, product, quantity, total):

	"""Добавляет продукты в заказ"""

	try:
		line = order.lines.get(product=product)
		line.quantity += quantity
		line.sub_total = total
		line.save(update_fields=['quantity'])
	except OrderLine.DoesNotExist:
		product_name = product.name
		order.lines.create(
			product_name=product_name,
			quantity=quantity,
			product=product,
			# sub_total=total,
		)
