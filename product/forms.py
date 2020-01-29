from django import forms
from django.contrib.auth.decorators import permission_required
from .models import Product
from core.models import Comment


class ProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=0,
	                              initial=1, required=False)

class SearchForm(forms.Form):
	pass


class CommentForm(forms.ModelForm):
	print(4)
	class Meta:
		model = Comment
		fields = ['text', ]
		labels = {'text': 'Enter your comment'}
		widgets = {
			'text': forms.Textarea(attrs={'rows':2, 'cols':5}),
		}

