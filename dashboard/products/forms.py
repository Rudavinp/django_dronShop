from django import forms
from django.db.models import Q

from product.models import Attribute, AttributeValue, ProductType, Product, Category, ProductImage
from django.utils.text import slugify
from mptt.forms import TreeNodeChoiceField


class ProductTypeForm(forms.ModelForm):
    """
    Форма для типа продукта:
    дополнительно определено поле product_attribute, которое
    предоставляет выбор незанятых атрибутов в зависимости
    от создание это нового ProductType или изменение существующего.
    """

    product_attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.all(),
        required=False,
        label='Product attributes'
    )

    class Meta:
        model = ProductType
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['product_attributes'].queryset = self.fields['product_attributes'].queryset.filter(
                    Q(type_attribute__exact=self.instance) | Q(type_attribute__isnull=True)
            )
        else:
            self.fields['product_attributes'].queryset = self.fields['product_attributes'].queryset.filter(
                type_attribute__isnull=True
            )

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        new_product_attrs = self.cleaned_data.get('product_attributes', [])
        print(55, new_product_attrs)
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
        for attribue in self.avalilabel_attributes:
            default_fields = {
                'label': attribue.name,
                'required': False,
            }
            field = forms.ModelChoiceField(queryset=attribue.attribute_value.all(), **default_fields)
            self.fields[attribue.get_formfield_name()] = field

    def iter_atribute_fields(self):
        for attr in self.avalilabel_attributes:
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

    def clean(self):
        cleaned_data = super(AttributeValueForm, self).clean()
        attr = cleaned_data.get('attribute')
        name = cleaned_data.get('name')
        if name in [n.name for n in attr.attribute_value.all()]:
            raise forms.ValidationError('This name is already exist')

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name)
        super().save(commit=commit)


class ProductImageForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    class Meta:
        model = ProductImage
        exclude = ['product']