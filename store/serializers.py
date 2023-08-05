from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # collection = CollectionSerializer()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.15)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "price_with_tax",
            "inventory",
            "collection",
        ]


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, source="unit_price"
#     )
#     price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
#     # collection = CollectionSerializer() #return collection object {"id": 1, "title": "Summer collection"}
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name="collection_detail",
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.15)
