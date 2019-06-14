from django.core.paginator import Paginator, InvalidPage
from django.http import Http404


def get_paginator_items(items, paginate_by, page_number):
	if not page_number:
		page_number = 1
	paginator = Paginator(items, paginate_by)
	try:
		page_number = int(page_number)
	except ValueError:
		raise Http404('Страница не может быть переведена в число')

	try:
		items = paginator.page(page_number)
	except InvalidPage as err:
		raise Http404('Неверная страница {}: {}'.format(page_number, str(err)))

	return items

