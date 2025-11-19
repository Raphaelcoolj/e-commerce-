from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
# Models were commented out in models.py, so we MUST comment out the import here too.
# from .models import Product, CartItem, Order, OrderItem 
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, CreateUserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import F, Sum
from rest_framework import filters
# from .filters import ProductFilter # Must be commented out if it relies on Product model
from django.db import transaction 

# -------------------------------
# CreateUserView (Kept, as it only uses User/Serializer, not the deleted models)
# -------------------------------
class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Authenticated user views (TEMPORARILY COMMENTED OUT)
# -------------------------------
# class ProductListView(generics.ListAPIView):
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [AllowAny] 
#     # filterset_class = ProductFilter # Commented out due to Product dependency
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'description', 'price']
#     ordering_fields = ['price', 'name']

# class AddToCartView(generics.CreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class CartListView(generics.ListAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # return CartItem.objects.filter(user=self.request.user)
#         return [] # Return empty list to prevent crash

# class PlaceOrderView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         # Code commented out to prevent reference errors during table deletion
#         return Response({"detail": "Temporarily disabled for maintenance."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# class UserOrderListView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # return Order.objects.filter(user=self.request.user)
#         return [] # Return empty list to prevent crash

# -------------------------------
# Admin views (TEMPORARILY COMMENTED OUT)
# -------------------------------
# class AdminProductViewSet(viewsets.ModelViewSet):
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminUser]

# class AdminCartViewSet(viewsets.ReadOnlyModelViewSet):
#     # queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAdminUser]

# class AdminOrderViewSet(viewsets.ReadOnlyModelViewSet):
#     # queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminUser]
