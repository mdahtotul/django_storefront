from django.urls import path
from . import views

urlpatterns = [
    # path("", views.page_init),
    # path("", views.all_query_set),
    # path("", views.get_product),
    # path("", views.filter_product),
    # path("", views.complex_filter_product),
    # path("", views.sorting_product),
    # path("", views.limiting_products),
    # path("", views.selecting_fields),
    # path("", views.deferring_fields),
    path("", views.selecting_related_objects),
    path("hello/", views.render_store_html),
]
