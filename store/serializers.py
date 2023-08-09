from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    # products_count = serializers.IntegerField(required=False)
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]
        # extra_kwargs = {
        #     "products_count": {"required": False},
        # }


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


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


"""
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source="unit_price"
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = CollectionSerializer() #return collection object {"id": 1, "title": "Summer collection"}
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name="collection_detail",
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.15)
"""


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField(method_name="calculate_total")

    def calculate_total(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "product", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    items = CartItemSerializer(many=True, read_only=True)

    grand_total_price = serializers.SerializerMethodField(method_name="calculate_total")

    def calculate_total(self, cart: Cart):
        return sum([x.quantity * x.product.unit_price for x in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total_price"]
