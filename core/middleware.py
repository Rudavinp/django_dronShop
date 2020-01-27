from product.models import Category


def catalog_middleware(get_response):

    def middleware(request):
        categories = Category.objects.all()
        request.categories = categories
        response = get_response(request)
        return response

    return middleware