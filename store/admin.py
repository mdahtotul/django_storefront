from django.contrib import admin
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# to know further search for django modeladmin-options


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 15
    list_select_related = ["collection"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 15

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


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
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
        return super().get_queryset(request).annotate(products_count=Count("product"))


admin.site.register(models.Cart)
