from django.shortcuts import redirect
from django.conf import settings
from django.template.response import TemplateResponse
from .forms import SignupForm, LoginForm
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required


def signup(request):
	form = SignupForm(request.POST or None)
	if form.is_valid():
		form.save()
		f = form.cleaned_data
		password = form.cleaned_data.get('password')
		email = form.cleaned_data.get('email')
		user = auth.authenticate(
			request=request, email=email, password=password)
		if user:
			auth.login(request, user)
		return redirect('home',)

	ctx = {'form': form}
	return TemplateResponse(request, 'account/signup.html', ctx)


def login(request):
	print('login', request)
	kwargs = {
		'template_name': 'account/login.html',
		'authentication_form': LoginForm}
	kwargs1 = {
		'template_name': 'account/login.html',
		'authentication_form': LoginForm,
		'lol': 'kek',
		}
	arg = 4
	return django_views.LoginView.as_view(**kwargs)(request, **kwargs)


@login_required
def logout(request):
	auth.logout(request)
	messages.success(request, ('You have been successfully logged out.'))
	return redirect(settings.LOGIN_REDIRECT_URL)
