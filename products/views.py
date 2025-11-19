from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Product, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, CreateUserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.models import F, Sum
from rest_framework import filters
from .filters import ProductFilter


#from django.contrib.auth.models import User
#from django.http import JsonResponse

#def create_admin_user(request):
 #   try:
  #      if not User.objects.filter(username="emeka").exists():
   #         User.objects.create_superuser(
    #            username="emeka",
     #           email="ekehchukwuemeka375@gmail.com",
      #          password="test"
       #     )
        #    return JsonResponse({"status": "created", "message": "Admin user created"})
       # return JsonResponse({"status": "exists", "message": "Admin already exists"})
    #except Exception as e:
     #   return JsonResponse({"status": "error", "message": str(e)})

#from django.core.management import call_command

#def run_migrations(request):
#    try:
#        call_command("migrate")
#        return JsonResponse({"status": "ok", "message": "Migrations applied"})
 #   except Exception as e:
  #      return JsonResponse({"status": "error", "message": str(e)})



class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Authenticated user views
# -------------------------------

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
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

from django.db import transaction, models

class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.select_related('product').filter(user=user)
        
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"detail": f"Not enough stock for {item.product.name}. Available: {item.product.stock}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        
        order = Order.objects.create(user=user, status='processing') # Set initial status
        
        order_items_to_create = []
        for item in cart_items:
            order_items_to_create.append(
                OrderItem(order=order, product=item.product, quantity=item.quantity)
            )     OrderItem.objects.bulk_create(order_items_to_create)

       
        order.calculate_total() # This must happen after OrderItems are created
        cart_items.delete() # Clears the user's cart
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
