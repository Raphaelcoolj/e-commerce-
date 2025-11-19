from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Product, CartItem, Order, OrderItem 
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, CreateUserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import F, Sum
from rest_framework import filters
from .filters import ProductFilter 
from django.db import transaction 

# -------------------------------
# CreateUserView (Kept, as it only uses User/Serializer, not the deleted models)
# -------------------------------
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Authenticated user views
# -------------------------------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] 
    filterset_class = ProductFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'price']
    ordering_fields = ['price', 'name']

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        # Optimization: select_for_update locks the cart items and their related products 
        # to prevent a race condition where two users buy the last item simultaneously.
        cart_items = CartItem.objects.select_related('product').filter(user=user).select_for_update() 

        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Inventory Check (Correctly implemented by you)
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"detail": f"Not enough stock for {item.product.name}. Available: {item.product.stock}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(user=user, status='processing') 

        order_items_to_create = []
        product_updates = []

        for item in cart_items:
            order_items_to_create.append(
                OrderItem(order=order, product=item.product, quantity=item.quantity)
            )
            
            # 2. CRITICAL FIX: Prepare atomic stock reduction (F expression)
            # This ensures the stock is decremented at the database level.
            product_updates.append(
                Product.objects.filter(pk=item.product.pk).update(stock=F('stock') - item.quantity)
            )

        # 3. FIX: Correctly indented bulk_create call
        OrderItem.objects.bulk_create(order_items_to_create) 
        
        # Note: The `product_updates` list contains the results of the updates, 
        # but the atomic F() updates have already executed successfully within the transaction.

        order.calculate_total()
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# -------------------------------
# Admin views
# -------------------------------
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminCartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAdminUser]

class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
