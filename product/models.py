from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from core.models import SortedModel
from django.utils.text import slugify
from django.utils.encoding import smart_text
from text_unidecode import unidecode
from django.contrib.postgres.fields import HStoreField
from discount.models import Sale


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
                               on_delete=models.CASCADE)

    tree = TreeManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    @property
    def get_slug(self):
        return slugify(unidecode(self.name))
    # def get_absolute_url(self):
    # 	return reverse('shop:product_by_firm', args=[self.slug])


class ProductType(models.Model):
    name = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                     related_name='products', blank=True, null=True)
    name = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(verbose_name="На складе", default=0)
    slug = models.SlugField(max_length=200, db_index=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    description = models.TextField(blank=True, default='')
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(validators=
                                   [MinValueValidator(0)], default=0)
    attributes = HStoreField(default=dict, blank=True)
    sale = models.ForeignKey(Sale, null=True, blank=True, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = (('manage_products', 'Manage products'), )

    def __str__(self):
        return self.name

    def get_image(self):
        product_image = ProductImage.objects.filter(product=self, is_main=True)
        if product_image:
            return product_image[0]

    @property
    def get_slug(self):
        return slugify(unidecode(self.name))

    def get_absolute_url(self):
        return reverse('product:product', kwargs={'slug': self.get_slug, 'product_id':self.id,})


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/',
                              blank=True, verbose_name="Изображение товара")
    is_main = models.BooleanField(default=False)

    class Meta:
        app_label = 'product'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class TypeAttribute(models.Model):
    name = models.CharField(max_length=200)
    product = models.ManyToManyField(Product, related_name='type_attribute')


class Attribute(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    type_attribute = models.ForeignKey(ProductType, blank=True, null=True,
                                       on_delete=models.CASCADE, related_name='attribute',
                                            )

    def __str__(self):
        return self.name

    def get_formfield_name(self):
        return slugify(
            'attribute-{}-{}'.format(self.slug, self.pk), allow_unicode=True
        )

class AttributeValue(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=300, blank=True, default='')
    slug = models.SlugField(max_length=200)
    attribute = models.ForeignKey(Attribute, blank=True, null=True,
                                  on_delete=models.CASCADE, related_name='attribute_value')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.attribute.attribute_value.all()