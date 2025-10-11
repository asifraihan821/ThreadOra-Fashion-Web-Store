from order import models
from django.db import transaction
from rest_framework.exceptions import PermissionDenied,ValidationError


class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = models.Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()

            total_price = sum([item.product.price *item.quantity for item in cart_items])

            order = models.Order.objects.create(user_id=user_id, total_price=total_price)

            order_items = [
                models.OrderItem(
                    order = order,
                    product = item.product,
                    price = item.price,
                    quantity = item.quantity,
                    total_price = item.product.price * item.quantity
                ) for item in cart_items
            ]

            models.OrderItem.objects.bulk_create(order_items)
            cart.delete()

            return order
        
    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            order.status = models.Order.CANCELLED
            order.save()
            return order
        elif order.user != user:
            raise PermissionDenied({'detail':'You can only cancel your own order'})
        elif order.status == models.Order.DELIVERED:
            raise ValidationError({'detail':'You cannot cancel delivered order'})
        
        order.status = models.Order.CANCELLED
        order.save()
        return order