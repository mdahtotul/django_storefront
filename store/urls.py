from django.urls import path
from store import views

urlpatterns = [
    # products
    path("products/", views.ProductList.as_view(), name="product_list"),
    path("products/<int:id>/", views.ProductDetail.as_view(), name="product_detail"),
    # collections
    path("collections/", views.CollectionList.as_view(), name="collection_list"),
    path(
        "collections/<int:pk>",
        views.CollectionDetail.as_view(),
        name="collection_detail",
    ),
]
