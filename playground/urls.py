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
    # path("", views.selecting_related_objects),
    # path("", views.aggregate_objects),
    # path("", views.annotating_objects),
    # path("", views.using_db_functions),
    # path("", views.grouping_data),
    # path("", views.expression_wrappers),
    # path("", views.generic_relationship),
    path("", views.custom_managers),
    path("hello/", views.render_store_html),
]
