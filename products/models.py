from django.db import models
from django.contrib.auth.models import User
# CRITICAL IMPORT: Needed for robust aggregation logic (Case/When)
from django.db.models import Sum, F, Case, When, DecimalField 

# -------------------------------
# Product
# -------------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    # The 'fancy' discounted price
    side_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) 

    @property
    def in_stock(self):
        return self.stock > 0
    
    @property
    def final_price(self):
        """Returns the discounted price (side_price) if set, otherwise returns the original price."""
        # Use side_price for calculations/charging if it exists.
        return self.side_price if self.side_price is not None else self.price

    def __str__(self):
        return self.name


# -------------------------------
# CartItem
# -------------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} ({self.user.username})"

    def total_price(self):
        # CORRECTION: Use the Product's final_price property for accurate cost
        return self.product.final_price * self.quantity

# -------------------------------
# Order
# -------------------------------
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {getattr(self.user, 'username', 'Unknown')}"


    def calculate_total(self):
        """Calculates the total price by using side_price (discount) if available, otherwise using price."""
        # CORRECTION: Use Case/When for database-level conditional price aggregation
        total_aggregate = self.items.aggregate(
            total=Sum(
                Case(
                    When(
                        # Check if the product's side_price is NOT NULL
                        product__side_price__isnull=False, 
                        # If side_price exists, use it
                        then=F('quantity') * F('product__side_price')
                    ),
                    # Otherwise, use the original price
                    default=F('quantity') * F('product__price'),
                    output_field=DecimalField()
                )
            )
        )
        self.total_price = total_aggregate['total'] or 0
        self.save()
        
    def update_inventory(self):
        """Reduces the stock count for each product in the order atomically (used in Admin/Views)."""
        for item in self.items.all():
            # Atomically update stock using F expression
            Product.objects.filter(pk=item.product_id).update(stock=F('stock') - item.quantity)


# -------------------------------
# OrderItem
# -------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
