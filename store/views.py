from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from store.serializers import ProductsSerializers


@api_view()
def product_list(req):
    queryset = Product.objects.select_related("collection").all()
    serializer = ProductsSerializers(queryset, many=True, context={"request": req})
    return Response(serializer.data)


@api_view()
def product_detail(req, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductsSerializers(product)
    data = serializer.data
    return Response(data)


@api_view()
def collection_detail(req, pk):
    return Response("ok")
