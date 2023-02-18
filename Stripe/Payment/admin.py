from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart_name', ]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['currency', 'percent_off', 'duration', 'duration_in_months', ]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['category', ]
