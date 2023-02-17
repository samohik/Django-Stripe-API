from django.contrib import admin
from .models import Item, Order


@admin.register(Item)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', ]


@admin.register(Order)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['cart', ]
