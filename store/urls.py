from django.urls import path
from store import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:id>/", views.product_detail, name="product_detail"),
]
