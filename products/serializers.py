from rest_framework import serializers
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth.models import User

# -------------------------------
# Product Serializer
# -------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# -------------------------------
# CartItem Serializer
# -------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']

# -------------------------------
# OrderItem Serializer
# -------------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# -------------------------------
# Order Serializer
# -------------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='items', many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'items', 'created_at']


# -------------------------------
# Serializer for creating users
# -------------------------------
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
