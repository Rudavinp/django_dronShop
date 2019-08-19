from django.shortcuts import render
from django.template.response import TemplateResponse

def index(request):
	return TemplateResponse(request, 'dashboard/new_base.html')

