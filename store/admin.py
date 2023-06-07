from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'created')
    list_filter = ('category',)
    list_display_links = ('id', 'name', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer',   'complete')
    list_display_links = ('id', 'customer', )
    list_filter = ('complete',)
    list_editable = ('complete',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'created')
    list_display_links = ('id', 'product', 'order',)


admin.site.register(ProductShots)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity','transaction_id', 'created')
    list_display_links = ('id', 'product', 'order',)
