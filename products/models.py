#from django.db import models
#from django.contrib.auth.models import User
# CRITICAL IMPORT: Needed for robust aggregation logic (Case/When)
#from django.db.models import Sum, F, Case, When, DecimalField 

# -------------------------------
# Product (TEMPORARILY COMMENTED OUT FOR DATABASE CLEANUP)
# -------------------------------
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField(default=0)
#     image = models.ImageField(upload_to='products/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # The 'fancy' discounted price
#     side_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 

#     @property
#     def in_stock(self):
#         return self.stock > 0

#     @property
#     def final_price(self):
#         """Returns the discounted price (side_price) if set, otherwise returns the original price."""
#         # Use side_price for calculations/charging if it exists.
#         return self.side_price if self.side_price is not None else self.price

#     def __str__(self):
#         return self.name


# -------------------------------
# CartItem (TEMPORARILY COMMENTED OUT FOR DATABASE CLEANUP)
# -------------------------------
# class CartItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE) # Commented due to Product being commented
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         # Modified to avoid accessing the product attribute which is now commented
#         return f"CartItem x {self.quantity} ({self.user.username})"

#     # def total_price(self):
#     #     # This method would fail without Product, so it's commented
#     #     return self.product.final_price * self.quantity

# -------------------------------
# Order (TEMPORARILY COMMENTED OUT FOR DATABASE CLEANUP)
# -------------------------------
# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     # products = models.ManyToManyField(Product, through='OrderItem') # Commented due to Product being commented
#     total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} - {getattr(self.user, 'username', 'Unknown')}"


#     def calculate_total(self):
#         # Pass through methods to prevent runtime errors
#         pass 

#     def update_inventory(self):
#         # Pass through methods to prevent runtime errors
#         pass 


# -------------------------------
# OrderItem (TEMPORARILY COMMENTED OUT FOR DATABASE CLEANUP)
# -------------------------------
# class OrderItem(models.Model):
#     # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # Commented due to Order being commented
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE) # Commented due to Product being commented
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"OrderItem x {self.quantity}"
