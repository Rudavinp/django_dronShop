from .models import ProductInCart


# def get_cart_info(request):
# 	session_key = request.session.session_key
#
# 	products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
# 	product_total_nmb = products_in_cart.count()
#
# 	return locals()
