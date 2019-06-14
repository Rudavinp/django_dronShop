from django import forms
from django.utils.text import slugify
from product.models import Category



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['slug',]
        labels = {'name': 'catName',
                  'description': 'catDescription',
                  }


    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name, allow_unicode=True)
        instance = super().save(commit=commit)
        return instance