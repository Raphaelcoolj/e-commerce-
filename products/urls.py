from django.urls import path, include
from rest_framework.routers import DefaultRouter

# All dependent views MUST be commented out to prevent ImportError, 
# as the views themselves are commented out.
# from .views import (
#     ProductListView, AddToCartView, CartListView, PlaceOrderView, UserOrderListView,
#     AdminProductViewSet, AdminCartViewSet, AdminOrderViewSet
# )

router = DefaultRouter()
# Router registrations must also be commented out.
# router.register('admin/products', AdminProductViewSet, basename='admin-product')
# router.register('admin/carts', AdminCartViewSet, basename='admin-cart')
# router.register('admin/orders', AdminOrderViewSet, basename='admin-order')

urlpatterns = [
    # All paths that reference the deleted views must be commented out.
    # path('products/', ProductListView.as_view(), name='products'),
    # path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/', CartListView.as_view(), name='cart'),
    # path('order/place/', PlaceOrderView.as_view(), name='place-order'),
    # path('orders/', UserOrderListView.as_view(), name='user-orders'),

    # Admin: Router inclusion must be commented out.
    # path('admin-api/', include(router.urls)),
]

# Note: Your file contained duplicate definitions of urlpatterns. 
# They are both commented out here for safety.
# urlpatterns = [
#     # path('products/', ProductListView.as_view(), name='products'),
#     # path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
#     # path('cart/', CartListView.as_view(), name='cart'),
#     # path('order/place/', PlaceOrderView.as_view(), name='place-order'),
#     # path('orders/', UserOrderListView.as_view(), name='user-orders'),

#     # path('admin-api/', include(router.urls)),
# ]
