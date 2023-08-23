from django.db import transaction
from decimal import Decimal
from rest_framework import serializers
from store.models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from store.signals import order_created


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
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    items = CartItemSerializer(many=True, read_only=True)

    grand_total_price = serializers.SerializerMethodField(method_name="calculate_total")

    def calculate_total(self, cart: Cart):
        return sum([x.quantity * x.product.unit_price for x in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # validate_<field_name>
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Product with this id does not exist")
        return value

    # override default save method
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # cart_item = CartItem.objects.create(
            #     cart_id=cart_id, product_id=product_id, quantity=quantity
            # )
            self.instance = cart_item = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class CreateOrderSerializer(serializers.Serializer):
    # if all of the code doesn't execute transaction method will rollback the changes in the database
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Cart with this id does not exist")
        elif CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError("Cart is empty")
        return value

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']

            customer = Customer.objects.get(user_id=user_id)

            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity,
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()
            
            order_created.send_robust(sender=self.__class__, order=order)
            
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']