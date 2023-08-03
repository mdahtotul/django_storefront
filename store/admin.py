from django.contrib import admin

from . import models

# to know further search for django modeladmin-options


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "unit_price", "inventory"]
    list_editable = ["unit_price", "inventory"]
    list_per_page = 15


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 15


# Register your models here.
admin.site.register(models.Collection)
admin.site.register(models.Cart)
