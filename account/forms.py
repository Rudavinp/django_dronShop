from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):
	password = forms.CharField(
		widget=forms.PasswordInput
	)
	email = forms.EmailField(
		error_messages={
			'unique': 'This email has already bin registred'
		}
	)
	class Meta:
		model = User
		fields = ('email', )

	def save(self, request=None, commit=True):
		user = super().save(commit=False)

		password = self.cleaned_data['password']
		user.set_password(password)
		if commit:
			user.save()
		return user


class LoginForm(AuthenticationForm):
	username = forms.EmailField(
		label='Email', max_length=75)

	def __init__(self, request=None, *args, **kwargs):
		super().__init__(request=request, *args, **kwargs)
		if request:
			print(40, request)
			email = request.GET.get('email')
			print(40, email)
			if email:
				self.fields['username'].initial = email

	error_messages = {
		'invalid_login': (
			"Please enter a correct %(username)s and password. Note that both "
			"fields may be case-sensitive."
		),
		'inactive': ("This account is inactive."),
	}