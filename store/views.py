from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


"""
# Getting ProductList or creating product without Generic Views
class ProductList(APIView):
    def get(self, req):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True, context={"request": req})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        serializer = ProductSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""


# Getting ProductList or creating product Generic Views
class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related("collection").all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


"""
# Getting Product or update or delete product without Generic Views
class ProductDetail(APIView):
    def get(self, req, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, req, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, req, id):
        product = get_object_or_404(Product, pk=id)
        if product.order_items.exists():
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
"""


# Getting Product or update or delete product with Generic Views
class ProductDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer

    # below we're overriding the default destroy method because it has some custom functions
    def delete(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.order_items.exists():
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


"""
# Getting CollectionList or creating collection without Generic Views
class CollectionList(APIView):
    def get(self, req):
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, req):
        serializer = CollectionSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""


# Getting CollectionList or creating collection with Generic Views
class CollectionList(ListCreateAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count("products")).all()

    def get_serializer_class(self):
        return CollectionSerializer


"""
# Getting Product or update or delete collection without Generic Views
class CollectionDetail(APIView):
    def get(self, req, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        serializer = CollectionSerializer(collection, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, req, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        if collection.products.exists():
            return Response(
                {
                    "error": "Collection cannot be deleted because it contains on or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count("products")).all()

    def get_serializer_class(self):
        return CollectionSerializer

    def delete(self, req, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count("products")), pk=pk
        )
        if collection.products.exists():
            return Response(
                {
                    "error": "Collection cannot be deleted because it contains on or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
