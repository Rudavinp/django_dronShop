from .models import ProductInCart, Cart
from .utils import get_cart_from_request

def get_cart_info(request):
    # session_key = request.session.session_key
    # products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    # product_total_nmb = products_in_cart.count()
    cart = get_cart_from_request(request)

    return {'cart': cart}
    # return locals()
