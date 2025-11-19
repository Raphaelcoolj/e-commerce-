#from django.contrib import admin
#from .models import Product, CartItem, Order, OrderItem


# -------------------------------
# Product (TEMPORARILY COMMENTED OUT FOR DB CLEANUP)
# -------------------------------
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     # ENHANCEMENT: Added 'stock' and 'side_price' (your discount field)
#     list_display = ('id', 'name', 'price', 'side_price', 'stock', 'created_at')
#     search_fields = ('name', 'description')
#     list_filter = ('created_at',)
#     # ENHANCEMENT: Allows quick editing of these crucial fields
#     list_editable = ('price', 'side_price', 'stock') 


# -------------------------------
# CartItem (TEMPORARILY COMMENTED OUT FOR DB CLEANUP)
# -------------------------------
# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'product', 'quantity', 'added_at')
#     list_filter = ('user', 'product')
#     search_fields = ('user__username', 'product__name')

# -------------------------------
# OrderItem Inline (TEMPORARILY COMMENTED OUT FOR DB CLEANUP)
# -------------------------------
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     readonly_fields = ('product', 'quantity')

# -------------------------------
# Order (TEMPORARILY COMMENTED OUT FOR DB CLEANUP)
# -------------------------------
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'status', 'total_price', 'created_at')
#     list_filter = ('status', 'user')
#     search_fields = ('user__username',)
#     inlines = [OrderItemInline]
#     readonly_fields = ('total_price',)  # make total_price read-only

#     # automatically calculate total price whenever order is saved in admin
#     def save_model(self, request, obj, form, change):
#         obj.calculate_total()
#         super().save_model(request, obj, form, change)
