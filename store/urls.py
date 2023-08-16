from cgitb import lookup
from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")
router.register("carts", views.CartViewSet, basename="carts")
router.register("customers", views.CustomerViewSet, basename="customers")

# products nested router
# route will look like - /products/1/reviews/
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
# carts nested router
# route will look like - /carts/<cart_id>/items/<cart_items_id>
carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = router.urls + products_router.urls + carts_router.urls

"""
# urlpatterns without ModelViewSet
urlpatterns = [
    # products
    path("products/", views.ProductList.as_view(), name="product_list"),
    path("products/<int:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    # collections
    path("collections/", views.CollectionList.as_view(), name="collection_list"),
    path(
        "collections/<int:pk>",
        views.CollectionDetail.as_view(),
        name="collection_detail",
    ),
]
"""
