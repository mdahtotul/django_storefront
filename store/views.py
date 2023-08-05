from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


@api_view(["GET", "POST"])
def product_list(req):
    if req.method == "GET":
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True, context={"request": req})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif req.method == "POST":
        serializer = ProductSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(req, id):
    product = get_object_or_404(Product, pk=id)

    if req.method == "GET":
        serializer = ProductSerializer(product)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)
    elif req.method == "PUT":
        serializer = ProductSerializer(product, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    elif req.method == "DELETE":
        if product.order_items.exists():
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def collection_list(req):
    if req.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(queryset, many=True)

        return Response(serializer.data)
    elif req.method == "POST":
        serializer = CollectionSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(req, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=pk
    )

    if req.method == "GET":
        serializer = CollectionSerializer(collection)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif req.method == "PUT":
        serializer = CollectionSerializer(collection, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif req.method == "DELETE":
        if collection.products.exists():
            return Response(
                {
                    "error": "Collection cannot be deleted because it contains on or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serializer = collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
