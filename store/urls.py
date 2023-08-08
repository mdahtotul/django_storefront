from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet, basename="collections")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = router.urls + products_router.urls

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
