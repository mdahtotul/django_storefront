from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer


@api_view(["GET", "POST"])
def product_list(req):
    if req.method == "GET":
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True, context={"request": req})
        return Response(serializer.data)
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

        return Response(data)
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


@api_view()
def collection_detail(req, pk):
    return Response("ok")
