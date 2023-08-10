from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core_custom.models import User
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


class TagInLine(GenericTabularInline):
    autocomplete_fields = ["tag"]
    extra = 0
    min_num = 1
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
