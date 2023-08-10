from typing import Any
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# to know further search for django modeladmin-options

"""
admin
12345
"""


# InventoryFilter is a custom filter that will be used in the admin panel to filter the products in products page
class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, req, model_admin):
        return [("<10", "Low")]

    def queryset(self, req, query_set: QuerySet[Any]):
        if self.value() == "<10":
            return query_set.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]
    autocomplete_fields = ["collection"]
    list_display = [
        "id",
        "title",
        "unit_price",
        "inventory",
        "inventory_status",
        "collection_title",
    ]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 15
    list_select_related = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title__istartswith"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, req, query_set: QuerySet[Any]):
        updated_count = query_set.update(inventory=0)
        self.message_user(
            req, f"{updated_count} products were successfully cleared", messages.INFO
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 15
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "payment_status", "customer_title"]
    list_editable = ["payment_status"]
    ordering = ["-placed_at"]
    list_per_page = 15
    list_select_related = ["customer"]

    def customer_title(self, order):
        return order.customer.first_name + " " + order.customer.last_name


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "products_count"]
    search_fields = ["title__istartswith"]

    """
    reverse(app_model_page) -> to get the url of an app followed by the model page
    ? -> to add query parameters for filtering
    urlencode({"collection__id": str(collection.id)}) -> to add the query parameter to the url
    """

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html("<a href='{}' >{}</a>", url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))


admin.site.register(models.Cart)
