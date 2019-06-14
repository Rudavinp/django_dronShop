from django import forms

from product.models import Attribute, AttributeValue, ProductType, Product, Category
from django.utils.text import slugify
from mptt.forms import TreeNodeChoiceField

class ProductTypeForm(forms.ModelForm):
    product_attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.all(), required=False,
        label='Product attributes'
    )
    class Meta:
        model = ProductType
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unassignes_attrs = Attribute.objects.all()
        self.fields['product_attributes'].queryset = unassignes_attrs

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        new_product_attrs = self.cleaned_data.get('product_attributes', [])
        instance.attribute.set(new_product_attrs)
        return instance


class ProductForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(),
                                   label='Category')
    def attribute_save(self):
        attributes = {}
        for attr in self.avalilabel_attributes:
            value = self.cleaned_data[attr.get_formfield_name()]
            if value:
                attributes[attr.name] = value.name
        return attributes



    class Meta:
        model = Product
        exclude = ['product_type', 'slug', 'create', 'update', 'discount', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_type = self.instance.product_type
        self.avalilabel_attributes = product_type.attribute.prefetch_related('attribute_value').all()
        print(99999, self.avalilabel_attributes)
        for attribue in self.avalilabel_attributes:
            default_fields = {
                'label': attribue.name,
                'required': False,
            }
            field = forms.ModelChoiceField(queryset=attribue.attribute_value.all(), **default_fields)
            self.fields[attribue.get_formfield_name()] = field

    def iter_atribute_fields(self):
        for attr in self.avalilabel_attributes:
            print(11110000, self[attr.get_formfield_name()].name)
            yield self[attr.get_formfield_name()]

    def save(self, commit=True):
        attributes = self.attribute_save()
        self.instance.attributes = attributes
        instance = super().save()
        return instance


class ProductChoiceTypeForm(forms.Form):
    types = forms.ModelChoiceField(queryset=ProductType.objects.all(),
                                   label='ProductType',
                                   widget=forms.RadioSelect, empty_label=None)


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        exclude = ['type_attribute']
        labels = {
            'name': 'Product display name',
            'slug': 'Product internal name',
        }


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['name', 'attribute']
        labels = {'name': 'Item name'}

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name)
        super().save(commit=commit)
