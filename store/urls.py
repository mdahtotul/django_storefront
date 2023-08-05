from django.urls import path
from store import views

urlpatterns = [
    # products
    path("products/", views.product_list, name="product_list"),
    path("products/<int:id>/", views.product_detail, name="product_detail"),
    # collections
    path("collections/", views.collection_list, name="collection_list"),
    path("collections/<int:pk>", views.collection_detail, name="collection_detail"),
]
