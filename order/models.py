
from django.db import models
from uuid import uuid4
from product.models import Product
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from account.models import User
from uuid import uuid4
from account.models import Address

class OrderStatus(models.Model):
    DRAFT = 'draft'
    UNFULFILLED = 'unfulfilled'
    PARTIALLY_FULFILLED = 'partially fulfilled'
    FULFILLED = 'fulfilled'
    CANCELED = 'canceled'

    CHOICES = [
        (DRAFT,
            'Status for a fully editable, not confirmed order created by '
           ),
        (UNFULFILLED,
            'Status for an order with any items marked as fulfilled'),
        (PARTIALLY_FULFILLED,
            'Status for an order with some items marked as fulfilled'),
        (FULFILLED,
            'Status for an order with all items marked as fulfilled'),
        (CANCELED,
            'Status for a permanently canceled order')]


class Order(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True,
        default=None, related_name='orders', on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=32, default=OrderStatus.UNFULFILLED,
        choices=OrderStatus.CHOICES)
    created = models.DateTimeField(
        default=now, editable=False
    )
    tracking_client_id = models.CharField(
        max_length=36, blank=True, editable=False)
    user_email = models.EmailField(blank=True, default='')
    token = models.CharField(max_length=36, unique=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='+', editable=False,
                                        null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)


    class Meta:
        ordering = ('-pk',)

    def __repr__(self):
        return '<Order #{}'.format(self.id)

    def __str__(self):
        return '#{}'.format(self.id)

    def __iter__(self):
        return iter(self.lines.all())


    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid4())
        return super().save(*args, **kwargs)


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, related_name='lines', editable=False, on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="+", on_delete=models.SET_NULL,
        blank=True, null=True
    )
    product_name = models.CharField(max_length=386)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)]
    )
    customer_note = models.TextField(blank=True, default='')
    sub_total = models.DecimalField(max_digits=9, decimal_places=2, default=0)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)



def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)



# class ProductInCart(models.Model):
#     session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
#     order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
#     nmb = models.IntegerField(default=1)
#     price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
#     is_active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#
#     def __str__(self):
#         return "%s" % self.product.name
#
#     class Meta:
#         verbose_name = 'Товар в корзине'
#         verbose_name_plural = 'Товары в корзине'
#
#
#     def save(self, *args, **kwargs):
#         price_per_item = self.product.price
#         self.price_per_item = price_per_item
#         self.total_price = int(self.nmb) * price_per_item
#
#         super(ProductInCart, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', null=True, blank=True,
                             on_delete=models.CASCADE)
    token = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True, default='')
    email = models.EmailField(blank=True, default='')
    billing_address = models.ForeignKey(
        Address, related_name='+', editable=False, null=True,
        on_delete=models.SET_NULL)

    def __len__(self):
        return self.product_in_cart.count()

    def __iter__(self):
        return iter(self.product_in_cart.all())

    def get_total(self):
        subtotal = (line.get_total_price() for line in self)
        return sum(subtotal)



class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, null=True, related_name='product_in_cart',
                             on_delete=models.CASCADE )
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999)], default=0
    )

    def __str__(self):
        return self.product.name

    def get_total_price(self):
        amount = self.quantity * self.product.price
        return amount
