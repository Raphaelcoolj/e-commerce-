from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView, AddToCartView, CartListView, PlaceOrderView, UserOrderListView,
    AdminProductViewSet, AdminCartViewSet, AdminOrderViewSet
)

router = DefaultRouter()
router.register('admin/products', AdminProductViewSet)
router.register('admin/carts', AdminCartViewSet)
router.register('admin/orders', AdminOrderViewSet)

urlpatterns = [
    # Authenticated users
    path('products/', ProductListView.as_view(), name='products'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/', UserOrderListView.as_view(), name='user-orders'),

    # Admin
    path('admin-api/', include(router.urls)),
]
