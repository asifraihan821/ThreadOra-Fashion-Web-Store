from django.db import models
from django.conf import settings
from product.models import Product
from users.models import User,Address
from uuid import uuid4

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Cart of {self.user.first_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'product'],]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    

class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED','Cancelled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4,editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order {self.id} by {self.user.first_name} - {self.status}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product.name} X {self.quantity}"