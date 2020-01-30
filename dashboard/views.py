from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def index(request):
	return TemplateResponse(request, 'dashboard/new_base.html')

