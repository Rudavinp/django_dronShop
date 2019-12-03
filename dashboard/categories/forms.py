from django import forms
from django.utils.text import slugify
from product.models import Category



class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.ancestor = kwargs.pop('ancestor')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Category
        exclude = ['slug',]
        labels = {'name': 'catName',
                  'description': 'catDescription',
                  }


    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name, allow_unicode=True)
        if self.ancestor:
            self.instance.parent = self.ancestor
        instance = super().save(commit=commit)
        return instance