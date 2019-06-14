
from django.contrib import admin
from .models import *


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0

class OrderProductsInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

# class StatusAdmin (admin.ModelAdmin):
#     list_display = [field.name for field in Status._meta.fields]
#
#     class Meta:
#         model = Status
#
# admin.site.register(Status, StatusAdmin)


class OrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ OrderProductsInLine]

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)


class ProductInOrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder

admin.site.register(ProductInOrder, ProductInOrderAdmin)

class OrderProducts(admin.ModelAdmin):
    list_display = [field.name for field in OrderLine._meta.fields]

    class Meta:
        model = OrderLine


class ProductInCartAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInCart._meta.fields]

    class Meta:
        model = ProductInCart

admin.site.register(ProductInCart, ProductInCartAdmin)